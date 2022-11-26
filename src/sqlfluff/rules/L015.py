"""Implementation of Rule L015."""
from typing import Optional

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler
from sqlfluff.core.rules.doc_decorators import document_fix_compatible, document_groups
from sqlfluff.utils.functional import sp, FunctionalContext
from sqlfluff.utils.reflow.sequence import ReflowSequence


@document_groups
@document_fix_compatible
class Rule_L015(BaseRule):
    """``DISTINCT`` used with parentheses.

    **Anti-pattern**

    In this example, parentheses are not needed and confuse
    ``DISTINCT`` with a function. The parentheses can also be misleading
    about which columns are affected by the ``DISTINCT`` (all the columns!).

    .. code-block:: sql

        SELECT DISTINCT(a), b FROM foo

    **Best practice**

    Remove parentheses to be clear that the ``DISTINCT`` applies to
    both columns.

    .. code-block:: sql

        SELECT DISTINCT a, b FROM foo

    """

    groups = ("all", "core")
    crawl_behaviour = SegmentSeekerCrawler({"select_clause", "function"})

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Looking for DISTINCT before a bracket.

        Look for DISTINCT keyword immediately followed by open parenthesis.
        """
        seq = None
        anchor = None
        children = FunctionalContext(context).segment.children()
        if context.segment.is_type("select_clause"):
            # Look for `select_clause_modifier`
            modifier = children.select(sp.is_type("select_clause_modifier"))
            first_element = children.select(sp.is_type("select_clause_element")).first()
            expression = (
                first_element.children(sp.is_type("expression")).first()
                or first_element
            )
            bracketed = expression.children(sp.is_type("bracketed")).first()
            # is the first element only an expression with only brackets?
            if modifier and bracketed:
                # If there's nothing else in the expression, remove the brackets.
                if len(expression[0].segments) == 1:
                    anchor, seq = self._remove_unneeded_brackets(context, bracketed)
                # Otherwise, still make sure there's a space after the DISTINCT.
                else:
                    anchor = modifier[0]
                    seq = ReflowSequence.from_around_target(
                        modifier[0],
                        context.parent_stack[0],
                        config=context.config,
                        sides="after",
                    )
        elif context.segment.is_type("function"):
            # Look for a function call DISTINCT()
            function_name = children.select(sp.is_type("function_name")).first()
            bracketed = children.first(sp.is_type("bracketed"))
            if (
                not function_name
                or function_name[0].raw_upper != "DISTINCT"
                or not bracketed
            ):
                return None
            anchor, seq = self._remove_unneeded_brackets(context, bracketed)
        if seq and anchor:
            # Get modifications.
            fixes = seq.respace().get_fixes()
            if fixes:
                return LintResult(
                    anchor=anchor,
                    fixes=fixes,
                )
        return None

    def _remove_unneeded_brackets(self, context, bracketed):
        # Remove the brackets and strip any meta segments.
        anchor = bracketed.get()
        assert anchor
        seq = ReflowSequence.from_around_target(
            anchor,
            context.parent_stack[0],
            config=context.config,
            sides="before",
        ).replace(anchor, self.filter_meta(anchor.segments)[1:-1])
        return anchor, seq
