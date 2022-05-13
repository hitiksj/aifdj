"""Implementation of Rule L065."""
from typing import List, Optional

import sqlfluff.core.rules.functional.segment_predicates as sp
from sqlfluff.core.parser import NewlineSegment
from sqlfluff.core.parser.segments.base import BaseSegment
from sqlfluff.core.rules.base import BaseRule, LintFix, LintResult, RuleContext
from sqlfluff.core.rules.doc_decorators import document_fix_compatible, document_groups


@document_groups
@document_fix_compatible
class Rule_L065(BaseRule):
    """Set operators should be surrounded by newlines.

    **Anti-pattern**

    In this example, `UNION ALL` is not on a line ifself.

    .. code-block:: sql

        SELECT 'a' AS col UNION ALL
        SELECT 'b' AS col

    **Best practice**

    .. code-block:: sql

        SELECT 'a' AS col
        UNION ALL
        SELECT 'b' AS col

    """

    groups = ("all",)

    _target_elems = ("set_operator",)

    def _eval(self, context: RuleContext) -> List[LintResult]:
        """Set operators should be surrounded by newlines.

        For any set operator we check if there is any NewLineSegment in the non-code
        segments preceeding or following it.

        In particular, as part of this rule we allow multiple NewLineSegments.
        """
        segment = context.functional.segment

        expression = segment.children()
        set_operator_segments = segment.children(sp.is_type(*self._target_elems))
        results: List[LintResult] = []

        # If len(set_operator) == 0 this will essentially not run
        for set_operator in set_operator_segments:
            preceeding_code = (
                expression.reversed().select(start_seg=set_operator).first(sp.is_code())
            )
            following_code = expression.select(start_seg=set_operator).first(
                sp.is_code()
            )
            res = {
                "before": expression.select(
                    start_seg=preceeding_code.get(), stop_seg=set_operator
                ),
                "after": expression.select(
                    start_seg=set_operator, stop_seg=following_code.get()
                ),
            }

            newline_before_set_operator = res["before"].first(sp.is_type("newline"))
            newline_after_set_operator = res["after"].first(sp.is_type("newline"))

            # If there is a whitespace directly preceeding/following the set operator we
            # are replacing it with a newline later.
            preceeding_whitespace = res["before"].first(sp.is_type("whitespace")).get()
            following_whitespace = res["after"].first(sp.is_type("whitespace")).get()

            if newline_before_set_operator and newline_after_set_operator:
                continue
            elif not newline_before_set_operator and newline_after_set_operator:
                results.append(
                    LintResult(
                        anchor=set_operator,
                        description=(
                            "Set operators should be surrounded by newlines. "
                            f"Missing newline before set operator {set_operator.raw}."
                        ),
                        fixes=_generate_fixes(whitespace_segment=preceeding_whitespace),
                    )
                )
            elif newline_before_set_operator and not newline_after_set_operator:
                results.append(
                    LintResult(
                        anchor=set_operator,
                        description=(
                            "Set operators should be surrounded by newlines. "
                            f"Missing newline after set operator {set_operator.raw}."
                        ),
                        fixes=_generate_fixes(whitespace_segment=following_whitespace),
                    )
                )
            else:
                results.append(
                    LintResult(
                        anchor=set_operator,
                        description=(
                            "Set operators should be surrounded by newlines. "
                            "Missing newline before and after set operator "
                            f"{set_operator.raw}."
                        ),
                        # FIXME: Not sure how to make mypy happy here...
                        fixes=[  # type: ignore
                            *_generate_fixes(whitespace_segment=preceeding_whitespace),
                            *_generate_fixes(whitespace_segment=following_whitespace),
                        ],
                    )
                )

        return results


def _generate_fixes(
    whitespace_segment: BaseSegment,
) -> Optional[List[LintFix]]:

    if whitespace_segment:
        return [
            LintFix.replace(
                anchor_segment=whitespace_segment,
                # TODO: Should we also add WhitespaceSegment( ... )
                # here to deal with indentation? or leave this to other
                # rules?
                edit_segments=[NewlineSegment()],
            )
        ]
    else:
        return []
