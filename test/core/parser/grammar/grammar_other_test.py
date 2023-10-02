"""Tests for any other grammars.

NOTE: All of these tests depend somewhat on the KeywordSegment working as planned.
"""

import logging

import pytest

from sqlfluff.core.parser import KeywordSegment, StringParser, SymbolSegment
from sqlfluff.core.parser.context import ParseContext
from sqlfluff.core.parser.grammar import Anything, Delimited, Nothing
from sqlfluff.core.parser.grammar.noncode import NonCodeMatcher


@pytest.mark.parametrize(
    "token_list,min_delimiters,allow_gaps,allow_trailing,match_len",
    [
        # Basic testing (note diff to v1, no trailing whitespace.)
        (["bar", " \t ", ".", "    ", "bar"], 0, True, False, 5),
        (["bar", " \t ", ".", "    ", "bar", "    "], 0, True, False, 5),
        # Testing allow_trailing
        (["bar", " \t ", ".", "   "], 0, True, False, 1),  # NOTE: Diff to v1
        (["bar", " \t ", ".", "   "], 0, True, True, 3),  # NOTE: Diff to v1
        # Testing the implications of allow_gaps
        (["bar", " \t ", ".", "    ", "bar"], 0, True, False, 5),
        (["bar", " \t ", ".", "    ", "bar"], 0, False, False, 1),
        (["bar", " \t ", ".", "    ", "bar"], 1, True, False, 5),
        (["bar", " \t ", ".", "    ", "bar"], 1, False, False, 0),
        (["bar", ".", "bar"], 0, True, False, 3),
        (["bar", ".", "bar"], 0, False, False, 3),
        (["bar", ".", "bar"], 1, True, False, 3),
        (["bar", ".", "bar"], 1, False, False, 3),
        # Check we still succeed with something trailing right on the end.
        (["bar", ".", "bar", "foo"], 1, False, False, 3),
        # Check min_delimiters. There's a delimiter here, but not enough to match.
        (["bar", ".", "bar", "foo"], 2, True, False, 0),
    ],
)
def test__parser__grammar_delimited(
    min_delimiters,
    allow_gaps,
    allow_trailing,
    token_list,
    match_len,
    caplog,
    generate_test_segments,
    fresh_ansi_dialect,
):
    """Test the Delimited grammar when not code_only."""
    test_segments = generate_test_segments(token_list)
    g = Delimited(
        StringParser("bar", KeywordSegment),
        delimiter=StringParser(".", SymbolSegment),
        allow_gaps=allow_gaps,
        allow_trailing=allow_trailing,
        min_delimiters=min_delimiters,
    )
    ctx = ParseContext(dialect=fresh_ansi_dialect)
    with caplog.at_level(logging.DEBUG, logger="sqlfluff.parser"):
        # Matching with whitespace shouldn't match if we need at least one delimiter
        m = g.match(test_segments, 0, ctx)

    assert len(m) == match_len


def test__parser__grammar_anything_bracketed(
    generate_test_segments, fresh_ansi_dialect
):
    """Test the Anything grammar with brackets.

    NOTE: For most greedy semantics we don't instantiate inner brackets, but
    in the Anything grammar, the assumption is that we're not coming back to
    these segments later so we take the time to instantiate any bracketed sections.
    """
    bracket_segments = generate_test_segments(["(", "foo", "    ", ")", " ", "foo"])
    ctx = ParseContext(dialect=fresh_ansi_dialect)
    # Check that we can make it past the brackets
    match = Anything(terminators=[StringParser("foo", KeywordSegment)]).match(
        bracket_segments, 0, parse_context=ctx
    )
    assert len(match) == 4  # i.e. don't match the whitespace between ")" and "foo"
    result = match.apply(bracket_segments)
    # Check we successfully constructed a bracketed segment.
    assert result[2].is_type("bracketed")
    assert result[2].raw == "(foo    )"
    # Check that the unmatched segments is foo AND the whitespace
    assert len(result.unmatched_segments) == 2


@pytest.mark.parametrize(
    "terminators,match_length",
    [
        # No terminators, full match.
        ([], 6),
        # If terminate with foo - match length 1.
        (["foo"], 1),
        # If terminate with foof - unterminated. Match everything
        (["foof"], 6),
        # Greedy matching until the first item should return none
        (["bar"], 0),
        # NOTE: the greedy until "baar" won't match because baar is
        # a keyword and therefore is required to have whitespace
        # before it. In the test sequence "baar" does not.
        # See `greedy_match()` for details.
        (["baar"], 6),
    ],
)
def test__parser__grammar_anything_match(
    terminators, match_length, test_segments, fresh_ansi_dialect
):
    """Test the Anything grammar.

    NOTE: Anything combined with terminators implements the semantics
    which used to be implemented by `GreedyUntil`.
    """
    ctx = ParseContext(dialect=fresh_ansi_dialect)
    terms = [StringParser(kw, KeywordSegment) for kw in terminators]
    result = Anything(terminators=terms).match(test_segments, 0, parse_context=ctx)
    assert result.matched_slice == slice(0, match_length)
    assert result.matched_class is None  # We shouldn't have set a class


def test__parser__grammar_nothing_match(test_segments, fresh_ansi_dialect):
    """Test the Nothing grammar."""
    ctx = ParseContext(dialect=fresh_ansi_dialect)
    assert not Nothing().match(test_segments, 0, ctx)


def test__parser__grammar_noncode_match(test_segments, fresh_ansi_dialect):
    """Test the NonCodeMatcher."""
    ctx = ParseContext(dialect=fresh_ansi_dialect)
    # NonCode Matcher doesn't work with simple
    assert NonCodeMatcher().simple(ctx) is None
    # We should match one and only one segment
    match = NonCodeMatcher().match(test_segments, 1, parse_context=ctx)
    assert match
    assert match.matched_slice == slice(1, 2)
