"""Implementation of Rule L064."""

import sys
from typing import Optional

import regex

if sys.version_info < (3, 8):
    from typing_extensions import Final
else:
    from typing import Final

from sqlfluff.core.parser.segments.raw import CodeSegment
from sqlfluff.core.rules.base import BaseRule, LintFix, LintResult, RuleContext
from sqlfluff.core.rules.doc_decorators import (
    document_configuration,
    document_fix_compatible,
)

QUOTES_MAPPING: Final = {
    "single_quotes": {
        "common_name": "single quotes",
        "preferred_quote_char": "'",
        "alternate_quote_char": '"',
    },
    "double_quotes": {
        "common_name": "double quotes",
        "preferred_quote_char": '"',
        "alternate_quote_char": "'",
    },
}
# BigQuery string prefix characters.
STRING_PREFIX_CHARS: Final = "rbRB"


@document_configuration
@document_fix_compatible
class Rule_L064(BaseRule):
    r"""Consistent usage of preferred quotes for STRING datatype.

    Some databases allow single quotes as well as double quotes to express a STRING
    literal. Prefer one type of quotes as specified in rule setting. Falling back to
    alternate quotes to reduce escapes.

    Dollar quoted raw strings are excluded from this rule, as they are mostly used for
    literal UDF Body definitions.

    .. note::
       This rule was taken from `Black code style
       <https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#strings>`_
       .

       For this rule to work the user needs to settle on a preferred quoting style. This
       is controversial and users may have different opinions on whether single or
       double quotes are preferred.

       Additionally, this rule can be dangerous. If accidentally enabled for dialects
       that do not support single *and* double quotes automated fixes can potentially
       break working SQL code.

       This rule is disabled by default. It can be enabled with the
       ``force_enable = True`` flag.

    **Anti-pattern**

    .. code-block:: sql
       :force:

        select
            "abc",
            'abc',
            "\"",
            "abc" = 'abc'
        from foo

    **Best practice**

    Ensure all STRING literals use preferred quotes, unless escaping can be reduced by
    using alternate quotes.

    .. code-block:: sql
       :force:

        select
            "abc",
            "abc",
            '"',
            "abc" = "abc"
        from foo

    """

    config_keywords = ["preferred_string_quotes", "force_enable"]

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        # Config type hints
        self.preferred_string_quotes: str
        self.force_enable: bool

        if not self.force_enable:
            return LintResult()

        # Only care about quoted literal segments.
        if not context.segment.name == "quoted_literal":
            return None

        fixed_string = self._normalize_preferred_string_quotes(
            context.segment.raw,
            preferred_quote_char=QUOTES_MAPPING[self.preferred_string_quotes][
                "preferred_quote_char"
            ],
            alternate_quote_char=QUOTES_MAPPING[self.preferred_string_quotes][
                "alternate_quote_char"
            ],
        )

        if fixed_string != context.segment.raw:
            self.logger.debug(
                "Inconsistent use of preferred quote style. Use %s instead of %s.",
                fixed_string,
                context.segment.raw,
            )
            return LintResult(
                anchor=context.segment,
                fixes=[
                    LintFix.replace(
                        context.segment,
                        [
                            CodeSegment(
                                raw=fixed_string,
                                name="quoted_literal",
                                type="literal",
                            )
                        ],
                    )
                ],
                description=(
                    "Inconsistent use of preferred quote style '"
                    f"{QUOTES_MAPPING[self.preferred_string_quotes]['common_name']}"
                    "' for STRING datatype."
                ),
            )

        return None

    def _sub_twice(self, regex: regex.Pattern, replacement: str, original: str) -> str:
        """Replace `regex` with `replacement` twice on `original`.

        This is used by string normalization to perform replaces on overlapping matches.
        """
        return regex.sub(replacement, regex.sub(replacement, original))

    def _normalize_preferred_string_quotes(
        self, s: str, preferred_quote_char: str, alternate_quote_char: str
    ) -> str:
        """Prefer `preferred_quote_char` but only if it doesn't cause more escaping.

        Adds or removes backslashes as appropriate.
        """
        value = s.lstrip(STRING_PREFIX_CHARS)

        if value[:3] == preferred_quote_char * 3:
            # TODO: Are we not replacing unnecessary quotes here?
            return s
        elif value[0] == preferred_quote_char:
            # Quotes are alright already. But maybe we can remove some unnecessary
            # escapes or reduce the number of escapes using alternate_quote_char ?
            orig_quote = preferred_quote_char
            new_quote = alternate_quote_char
        elif value[:3] == alternate_quote_char * 3:
            orig_quote = alternate_quote_char * 3
            new_quote = preferred_quote_char * 3
        elif value[0] == alternate_quote_char:
            orig_quote = alternate_quote_char
            new_quote = preferred_quote_char
        else:
            self.logger.debug(
                "Found quoted string %s using neither preferred quote char %s "
                "nor alternate_quote_char %s. Skipping...",
                s,
                preferred_quote_char,
                alternate_quote_char,
            )
            return s

        first_quote_pos = s.find(orig_quote)
        prefix = s[:first_quote_pos]
        unescaped_new_quote = regex.compile(rf"(([^\\]|^)(\\\\)*){new_quote}")
        escaped_new_quote = regex.compile(rf"([^\\]|^)\\((?:\\\\)*){new_quote}")
        escaped_orig_quote = regex.compile(rf"([^\\]|^)\\((?:\\\\)*){orig_quote}")
        body = s[first_quote_pos + len(orig_quote) : -len(orig_quote)]

        if "r" in prefix.lower():
            if unescaped_new_quote.search(body):
                self.logger.debug(
                    "There's at least one unescaped new_quote in this raw string "
                    "so converting is impossible."
                )
                return s

            # Do not introduce or remove backslashes in raw strings
            new_body = body
        else:
            # remove unnecessary escapes
            new_body = self._sub_twice(escaped_new_quote, rf"\1\2{new_quote}", body)
            if body != new_body:
                # Consider the string without unnecessary escapes as the original
                self.logger.debug("Removing unnecessary escapes in %s.", body)
                body = new_body
                s = f"{prefix}{orig_quote}{body}{orig_quote}"
            new_body = self._sub_twice(
                escaped_orig_quote, rf"\1\2{orig_quote}", new_body
            )
            new_body = self._sub_twice(
                unescaped_new_quote, rf"\1\\{new_quote}", new_body
            )

        if (
            new_quote == 3 * preferred_quote_char
            and new_body[-1:] == preferred_quote_char
        ):
            # edge case: for example when converting quotes from '''a"'''
            # to """a\"""" the last " of the string body needs to be escaped.
            new_body = new_body[:-1] + f"\\{preferred_quote_char}"

        orig_escape_count = body.count("\\")
        new_escape_count = new_body.count("\\")
        if new_escape_count > orig_escape_count:
            self.logger.debug(
                "Changing quote style would introduce more escapes in the body. "
                "Before: %s After: %s . Skipping.",
                body,
                new_body,
            )
            return s  # Do not introduce more escaping

        if new_escape_count == orig_escape_count and orig_quote == preferred_quote_char:
            # Use preferred_quote_char
            return s

        return f"{prefix}{new_quote}{new_body}{new_quote}"
