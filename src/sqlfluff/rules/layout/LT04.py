"""Implementation of Rule LT04."""

from typing import List

from sqlfluff.core.rules import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.crawlers import SegmentSeekerCrawler
from sqlfluff.utils.reflow import ReflowSequence


class Rule_LT04(BaseRule):
    """Leading/Trailing comma enforcement.

    **Anti-pattern**

    There is a mixture of leading and trailing commas.

    .. code-block:: sql

        SELECT
            a
            , b,
            c
        FROM foo

    **Best practice**

    By default, `SQLFluff` prefers trailing commas. However it
    is configurable for leading commas. The chosen style must be used
    consistently throughout your SQL.

    .. code-block:: sql

        SELECT
            a,
            b,
            c
        FROM foo

        -- Alternatively, set the configuration file to 'leading'
        -- and then the following would be acceptable:

        SELECT
            a
            , b
            , c
        FROM foo
    """

    name = "layout.commas"
    aliases = ("L019",)
    groups = ("all", "layout")
    crawl_behaviour = SegmentSeekerCrawler({"comma"})
    _adjust_anchors = True
    is_fix_compatible = True

    def _eval(self, context: RuleContext) -> List[LintResult]:
        """Enforce comma placement.

        For the fixing routines we delegate to the reflow utils. However
        for performance reasons we have some initial shortcuts to quickly
        identify situations which are _ok_ to avoid the overhead of the
        full reflow path.
        """
        comma_positioning = context.config.get(
            "line_position", ["layout", "type", "comma"]
        )
        # NOTE: These shortcuts assume that any newlines will be direct
        # siblings of the comma in question. This isn't _always_ the case
        # but is true often enough to have meaningful upside from early
        # detection.
        parent = context.parent_stack[-1]
        idx = parent.segments.index(context.segment)

        # Shortcut #1: Leading.
        if comma_positioning == "leading":
            for segment in parent.segments[idx - 1 :: -1]:
                if segment.is_type("newline"):
                    # It's definitely leading. No problems.
                    self.logger.debug(
                        "Shortcut Leading OK. Found preceding newline: %s", segment
                    )
                    return [LintResult()]
                elif not segment.is_type("whitespace", "indent"):
                    # We found something before it which suggests it's not leading.
                    # We should run the full reflow routine to check.
                    break

        # Shortcut #2: Trailing.
        elif comma_positioning == "trailing":
            for segment in parent.segments[idx + 1 :]:
                if segment.is_type("newline"):
                    # It's definitely trailing. No problems.
                    self.logger.debug(
                        "Shortcut Trailing OK. Found following newline: %s", segment
                    )
                    return [LintResult()]
                elif not segment.is_type("whitespace", "indent"):
                    # We found something after it which suggests it's not trailing.
                    # We should run the full reflow routine to check.
                    break

        return (
            ReflowSequence.from_around_target(
                context.segment,
                root_segment=context.parent_stack[0],
                config=context.config,
            )
            .rebreak()
            .get_results()
        )
