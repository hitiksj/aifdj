"""Implementation of Rule L042."""
import copy
from functools import partial
from typing import (
    Generator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    cast,
)
from sqlfluff.core.dialects.base import Dialect
from sqlfluff.core.dialects.common import AliasInfo
from sqlfluff.core.parser.segments.base import BaseSegment
from sqlfluff.core.parser.segments.raw import (
    CodeSegment,
    KeywordSegment,
    NewlineSegment,
    SymbolSegment,
    WhitespaceSegment,
)
from sqlfluff.core.rules import BaseRule, LintFix, LintResult, RuleContext
from sqlfluff.core.rules.analysis.select import get_select_statement_info
from sqlfluff.core.rules.analysis.select_crawler import (
    Query,
    QueryType,
    SelectCrawler,
)
from sqlfluff.core.rules.doc_decorators import (
    document_configuration,
    document_fix_compatible,
    document_groups,
)
from sqlfluff.core.rules.functional.segment_predicates import (
    is_keyword,
    is_name,
    is_type,
    is_whitespace,
)
from sqlfluff.core.rules.functional.segments import Segments
from sqlfluff.dialects.dialect_ansi import (
    CTEDefinitionSegment,
    TableExpressionSegment,
    TableReferenceSegment,
    WithCompoundStatementSegment,
)


class _NestedSubQuerySummary(NamedTuple):
    parent_clause_type: str
    parent_select_segments: Segments
    clause_segments: Segments
    subquery: BaseSegment


@document_groups
@document_fix_compatible
@document_configuration
class Rule_L042(BaseRule):
    """Join/From clauses should not contain subqueries. Use CTEs instead.

    By default this rule is configured to allow subqueries within ``FROM``
    clauses but not within ``JOIN`` clauses. If you prefer a stricter lint
    then this is configurable.

    .. note::
       Some dialects don't allow CTEs, and for those dialects
       this rule makes no sense and should be disabled.

    **Anti-pattern**

    .. code-block:: sql

        select
            a.x, a.y, b.z
        from a
        join (
            select x, z from b
        ) using(x)


    **Best practice**

    .. code-block:: sql

        with c as (
            select x, z from b
        )
        select
            a.x, a.y, c.z
        from a
        join c using(x)

    """

    groups = ("all",)
    config_keywords = ["forbid_subquery_in"]

    _config_mapping = {
        "join": ["join_clause"],
        "from": ["from_expression_element"],
        "both": ["join_clause", "from_expression_element"],
    }

    def _eval(self, context: RuleContext) -> Optional[List[LintResult]]:
        """Join/From clauses should not contain subqueries. Use CTEs instead."""
        select_types = [
            "with_compound_statement",
            "set_expression",
            "select_statement",
        ]
        self.forbid_subquery_in: str
        parent_types = self._config_mapping[self.forbid_subquery_in]
        segment = context.functional.segment
        parent_stack = context.functional.parent_stack
        is_select = segment.all(is_type(*select_types))
        is_select_child = parent_stack.any(is_type(*select_types))
        if not is_select or is_select_child:
            # Nothing to do.
            return None

        # Gather all possible offending Elements in one crawl
        nested_subqueries: List[_NestedSubQuerySummary] = []
        selects = segment.recursive_crawl(*select_types, recurse_into=True)
        for select in selects.iterate_segments():
            for res in _find_nested_subqueries(select, context.dialect):
                if res.parent_clause_type not in parent_types:
                    continue
                nested_subqueries.append(res)
        crawler = SelectCrawler(context.segment, context.dialect)

        assert crawler.query_tree
        if not crawler.query_tree.children:
            return None

        # generate an instance which will track and shape our output CTE
        ctes = _CTEBuilder()
        # Init the output/final select &
        # populate existing CTEs
        for cte in crawler.query_tree.ctes.values():
            ctes.insert_cte(cte.cte_definition_segment)  # type: ignore

        is_with = segment.all(is_type("with_compound_statement"))
        # TODO: consider if we can fix recursive CTEs
        is_recursive = is_with and len(segment.children(is_name("recursive"))) > 0
        case_preference = _get_case_preference(segment)
        output_select = segment
        if is_with:
            output_select = segment.children(
                is_type(
                    "set_expression",
                    "select_statement",
                )
            )

        # If there are offending elements calculate fixes
        clone_map = SegmentCloneMap(segment[0])
        result = _calculate_fixes(
            dialect=context.dialect,
            query=crawler.query_tree,
            parent_stack=parent_stack,
            ctes=ctes,
            case_preference=case_preference,
            clone_map=clone_map,
        )

        if result:
            _, from_expression, alias_name, subquery_parent = result[-1]
            assert any(
                from_expression is seg for seg in subquery_parent.recursive_crawl_all()
            )
            this_seg_clone = clone_map[from_expression]
            new_table_ref = _create_table_ref(alias_name, context.dialect)
            this_seg_clone.segments = [new_table_ref]
            ctes.replace_with_clone(subquery_parent, clone_map)

            # Issue 3617: In T-SQL (and possibly other dialects) the automated fix
            # leaves parentheses in a location that causes a syntax error. This is an
            # unusual corner case. For simplicity, we still generate the lint warning
            # but don't try to generate a fix. Someone could look at this later (a
            # correct fix would involve removing the parentheses.)
            bracketed_ctas = [seg.type for seg in parent_stack[-2:]] == [
                "create_table_statement",
                "bracketed",
            ]
            if bracketed_ctas or ctes.has_duplicate_aliases() or is_recursive:
                # If we have duplicate CTE names just don't fix anything
                # Return the lint warnings anyway
                return [result[0] for result in result]

            # Add fixes to the last result only
            edit = [
                ctes.compose_select(
                    clone_map[output_select[0]],
                    case_preference=case_preference,
                ),
            ]
            result[-1][0].fixes = [
                LintFix.replace(
                    segment[0],
                    edit_segments=edit,
                )
            ]
            result = [result[0] for result in result]
        return result


def _calculate_fixes(
    dialect: Dialect,
    query: Query,
    parent_stack: Segments,
    ctes: "_CTEBuilder",
    case_preference,
    clone_map,
):  # -> List[LintResult]:
    """Given the Root select and the offending subqueries calculate fixes."""
    if not query.children:
        return []

    print(f"Query: {query.selectables[0].selectable.raw}")
    lint_results = []
    subquery_summary: _NestedSubQuerySummary
    for source in SelectCrawler.get(query, query.selectables[0].selectable):
        if isinstance(source, Query):
            lint_results.extend(
                _calculate_fixes(
                    dialect, source, parent_stack, ctes, case_preference, clone_map
                )
            )

    if query.query_type != QueryType.WithCompound:
        for child in query.children:
            for selectable in child.selectables:
                alias_name, is_new_name = ctes.create_cte_alias(
                    selectable.select_info.table_aliases
                )
                new_cte = _create_cte_seg(
                    alias_name=alias_name,
                    subquery=clone_map[selectable.selectable],
                    case_preference=case_preference,
                    dialect=dialect,
                )
                print(f"Creating new CTE: {new_cte.raw}")
                insert_position = ctes.insert_cte(new_cte)
                print(f"Inserted new CTE: {ctes.ctes[insert_position].raw}")
                from_expression = (
                    query.selectables[0]
                    .select_info.table_aliases[0]
                    .from_expression_element
                )
                # this_seg_clone = clone_map[from_expression]
                # new_table_ref = _create_table_ref(alias_name, dialect)
                # this_seg_clone.segments = [new_table_ref]
                anchor = from_expression.get_child("table_expression")
                # Grab the first keyword or symbol in the subquery to use as the
                # anchor. This makes the lint warning less likely to be filtered out
                # if a bit of the subquery happens to be templated.
                for seg in anchor.recursive_crawl("keyword", "symbol"):
                    anchor = seg
                    break
                res = LintResult(
                    anchor=anchor,
                    description=f"{query.selectables[0].selectable.type} clauses "
                    "should not contain subqueries. Use CTEs instead",
                    fixes=[],
                )
                lint_results.append(
                    (res, from_expression, alias_name, query.selectables[0].selectable)
                )
    return lint_results


def _get_first_select_statement_descendant(
    segment: BaseSegment,
) -> Optional[BaseSegment]:
    """Find first SELECT statement segment (if any) in descendants of 'segment'."""
    for select_statement in segment.recursive_crawl(
        "select_statement", recurse_into=False
    ):
        # We only want the first one.
        return select_statement
    return None  # pragma: no cover


def _get_sources_from_select(segment: BaseSegment, dialect: Dialect) -> Set[str]:
    """Given segment, return set of table or alias names it queries from."""
    result = set()
    select = None
    if segment.is_type("select_statement"):
        select = segment
    elif segment.is_type("with_compound_statement"):
        # For WITH statement, process the main query underneath.
        select = _get_first_select_statement_descendant(segment)
    if select and select.is_type("select_statement"):
        select_info = get_select_statement_info(select, dialect)
        if select_info:
            for a in select_info.table_aliases:
                # For each table in FROM, return table name and any alias.
                if a.ref_str:
                    result.add(a.ref_str)
                if a.object_reference:
                    result.add(a.object_reference.raw)
    return result


def _is_correlated_subquery(
    nested_select: Segments, select_source_names: Set[str], dialect: Dialect
):
    """Given nested select and the sources of its parent, determine if correlated.

    https://en.wikipedia.org/wiki/Correlated_subquery
    """
    if not nested_select:
        return False  # pragma: no cover
    select_statement = _get_first_select_statement_descendant(nested_select[0])
    if not select_statement:
        return False  # pragma: no cover
    nested_select_info = get_select_statement_info(select_statement, dialect)
    if nested_select_info:
        for r in nested_select_info.reference_buffer:
            for tr in r.extract_possible_references(  # type: ignore
                level=r.ObjectReferenceLevel.TABLE  # type: ignore
            ):
                # Check for correlated subquery, as indicated by use of a
                # parent reference.
                if tr.part in select_source_names:
                    return True
    return False


def _find_nested_subqueries(
    select: Segments,
    dialect: Dialect,
) -> Generator[_NestedSubQuerySummary, None, None]:
    """Find possible offending elements and return enough to fix them."""
    select_types = [
        "with_compound_statement",
        "set_expression",
        "select_statement",
    ]
    from_clause = select.children().first(is_type("from_clause")).children()
    offending_types = ["join_clause", "from_expression_element"]
    select_source_names = _get_sources_from_select(select[0], dialect)

    # Match any of the types we care about
    for this_seg in from_clause.children(is_type(*offending_types)).iterate_segments():
        parent_type = this_seg[0].get_type()
        # Ensure we are at the right depth (from_expression_element)
        if not this_seg.all(is_type("from_expression_element")):
            this_seg = this_seg.children(
                is_type("from_expression_element"),
            )

        table_expression_el = this_seg.children(
            is_type("table_expression"),
        )

        # Is it bracketed? If so, lint that instead.
        bracketed_expression = table_expression_el.children(
            is_type("bracketed"),
        )
        nested_select = bracketed_expression or table_expression_el
        # If we find a child with a "problem" type, raise an issue.
        # If not, we're fine.
        seg = nested_select.children(is_type(*select_types))
        if not seg:
            # If there is no match there is no error
            continue
        # Type, parent_select, parent_sequence
        if not _is_correlated_subquery(nested_select, select_source_names, dialect):
            yield _NestedSubQuerySummary(
                parent_type, select, this_seg, table_expression_el[0]
            )


class _CTEBuilder:
    """Gather CTE parts, maintain order and track naming/aliasing."""

    def __init__(self) -> None:
        self.ctes: List[CTEDefinitionSegment] = []
        self.name_idx = 0

    def list_used_names(self) -> List[str]:
        """Check CTEs and return used aliases."""
        used_names: List[str] = []
        for cte in self.ctes:
            id_seg = cte.get_identifier()
            cte_name = id_seg.raw
            if id_seg.is_name("quoted_identifier"):
                cte_name = cte_name[1:-1]

            used_names.append(cte_name)
        return used_names

    def has_duplicate_aliases(self) -> bool:
        used_names = self.list_used_names()
        return len(set(used_names)) != len(used_names)

    def insert_cte(self, cte: CTEDefinitionSegment) -> int:
        """Add a new CTE to the list as late as possible but before all its parents."""
        # This should still have the position markers of its true position
        inbound_subquery = (
            Segments(cte).children().last(lambda seg: bool(seg.pos_marker))
        )
        insert_position = next(
            (
                i
                for i, el in enumerate(self.ctes)
                if _is_child(Segments(el).children().last(), inbound_subquery)
            ),
            len(self.ctes),
        )

        self.ctes.insert(insert_position, cte)
        print("CTEs:")
        print("==========")
        print("\n\n".join(cte.raw for cte in self.ctes))
        return insert_position

    def create_cte_alias(self, aliases: List[AliasInfo]) -> Tuple[str, bool]:
        """Find or create the name for the next CTE."""
        if aliases and aliases[0].ref_str:
            # If we know the name use it
            return aliases[0].ref_str, False

        self.name_idx = self.name_idx + 1
        name = f"prep_{self.name_idx}"
        if name in self.list_used_names():
            # corner case where prep_x exists in origin query
            return self.create_cte_alias([])
        return name, True

    def get_cte_segments(self) -> List[BaseSegment]:
        """Return a valid list of CTES with required padding Segments."""
        cte_segments: List[BaseSegment] = []
        for cte in self.ctes:
            cte_segments = cte_segments + [
                cte,
                SymbolSegment(",", name="comma", type="comma"),
                NewlineSegment(),
            ]
        return cte_segments[:-2]

    def compose_select(self, output_select: BaseSegment, case_preference: str):
        """Compose our final new CTE."""
        # Ensure there's whitespace between "FROM" and the CTE table name.
        from_clause = output_select.get_child("from_clause")
        from_clause_children = Segments(*from_clause.segments)
        from_segment = from_clause_children.first(is_keyword("from"))
        if from_segment and not from_clause_children.select(
            start_seg=from_segment[0], loop_while=is_whitespace()
        ):
            idx_from = from_clause_children.index(from_segment[0])
            # Insert whitespace between "FROM" and the CTE table name.
            from_clause.segments = list(
                from_clause_children[: idx_from + 1]
                + (WhitespaceSegment(),)
                + from_clause_children[idx_from + 1 :]
            )

        # Compose the CTE.
        new_select = WithCompoundStatementSegment(
            segments=tuple(
                [
                    _segmentify("WITH", case_preference),
                    WhitespaceSegment(),
                    *self.get_cte_segments(),
                    NewlineSegment(),
                    output_select,
                ]
            )
        )
        return new_select

    def replace_with_clone(self, segment, clone_map):
        for idx, cte in enumerate(self.ctes):
            if any(segment is seg for seg in cte.recursive_crawl_all()):
                self.ctes[idx] = clone_map[self.ctes[idx]]
                return
        else:
            assert False


def _is_child(maybe_parent: Segments, maybe_child: Segments) -> bool:
    """Is the child actually between the start and end markers of the parent."""
    assert len(maybe_child) == 1, "Cannot assess Childness of multiple Segments"
    assert len(maybe_parent) == 1, "Cannot assess Childness of multiple Parents"
    child_markers = maybe_child[0].pos_marker
    parent_pos = maybe_parent[0].pos_marker
    if not parent_pos or not child_markers:
        return False  # pragma: no cover

    if child_markers < parent_pos.start_point_marker():
        return False  # pragma: no cover

    if child_markers > parent_pos.end_point_marker():
        return False

    return True


S = TypeVar("S", bound=Type[BaseSegment])


def _get_seg(class_def: S, dialect: Dialect) -> S:
    return cast(S, dialect.get_segment(class_def.__name__))


def _create_cte_seg(
    alias_name: str, subquery: BaseSegment, case_preference: str, dialect: Dialect
) -> CTEDefinitionSegment:
    CTESegment = _get_seg(CTEDefinitionSegment, dialect)
    element: CTEDefinitionSegment = CTESegment(
        segments=(
            CodeSegment(
                raw=alias_name,
                name="naked_identifier",
                type="identifier",
            ),
            WhitespaceSegment(),
            _segmentify("AS", casing=case_preference),
            WhitespaceSegment(),
            SymbolSegment("(", name="start_bracket", type="start_bracket"),
            subquery,
            SymbolSegment(")", name="end_bracket", type="end_bracket"),
        )
    )
    return element


def _create_table_ref(table_name: str, dialect: Dialect) -> TableExpressionSegment:
    Seg = partial(_get_seg, dialect=dialect)
    TableExpressionSeg = Seg(TableExpressionSegment)
    TableReferenceSeg = Seg(TableReferenceSegment)
    table_seg = TableExpressionSeg(
        segments=(
            TableReferenceSeg(
                segments=(
                    CodeSegment(
                        raw=table_name,
                        name="naked_identifier",
                        type="identifier",
                    ),
                ),
            ),
        ),
    )
    return table_seg  # type: ignore


def _get_case_preference(root_select: Segments):
    first_keyword = root_select.recursive_crawl(
        "keyword",
        recurse_into=False,
    ).first()[0]
    if first_keyword.raw[0].islower():
        return "LOWER"

    return "UPPER"


def _segmentify(input_el: str, casing: str) -> BaseSegment:
    """Apply casing and convert strings to Keywords."""
    input_el = input_el.lower()
    if casing == "UPPER":
        input_el = input_el.upper()

    return KeywordSegment(raw=input_el)


class SegmentCloneMap:
    """Clones a segment tree, maps from original segments to their clones."""

    def __init__(self, segment: BaseSegment):
        segment_copy = copy.deepcopy(segment)
        self.segment_map = {}
        for old_segment, new_segment in zip(
            segment.recursive_crawl_all(),
            segment_copy.recursive_crawl_all(),
        ):
            new_segment.pos_marker = old_segment.pos_marker
            self.segment_map[id(old_segment)] = new_segment

    def __getitem__(self, old_segment: BaseSegment) -> BaseSegment:
        return self.segment_map[id(old_segment)]
