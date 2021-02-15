"""The Test file for The New Parser (Grammar Classes)."""

import pytest
import logging

from sqlfluff.core.parser import KeywordSegment, ReSegment
from sqlfluff.core.parser.context import RootParseContext
from sqlfluff.core.parser.segments import EphemeralSegment
from sqlfluff.core.parser.grammar.base import BaseGrammar
from sqlfluff.core.parser.grammar.noncode import NonCodeMatcher
from sqlfluff.core.parser.grammar import (
    OneOf,
    Sequence,
    GreedyUntil,
    Delimited,
    StartsWith,
    Anything,
    Nothing,
)

# NB: All of these tests depend somewhat on the KeywordSegment working as planned


def make_result_tuple(result_slice, matcher_keywords, seg_list):
    """Make a comparison tuple for test matching."""
    # No result slice means no match.
    if not result_slice:
        return ()

    return tuple(
        KeywordSegment.make(elem.raw)(elem.raw, elem.pos_marker)
        if elem.raw in matcher_keywords
        else elem
        for elem in seg_list[result_slice]
    )


@pytest.mark.parametrize(
    "seg_list_slice,matcher_keywords,trim_noncode,result_slice",
    [
        # Matching the first element of the list
        (slice(None, None), ["bar"], False, slice(None, 1)),
        # Matching with a bit of whitespace before
        (slice(1, None), ["foo"], True, slice(1, 3)),
        # Matching with a bit of whitespace before (not trim_noncode)
        (slice(1, None), ["foo"], False, None),
        # Matching with whitespace after
        (slice(None, 2), ["bar"], True, slice(None, 2)),
    ],
)
def test__parser__grammar__base__longest_trimmed_match__basic(
    seg_list, seg_list_slice, matcher_keywords, trim_noncode, result_slice
):
    """Test the _longest_trimmed_match method of the BaseGrammar."""
    # Make the matcher keywords
    matchers = [KeywordSegment.make(keyword) for keyword in matcher_keywords]

    with RootParseContext(dialect=None) as ctx:
        m, _ = BaseGrammar._longest_trimmed_match(
            seg_list[seg_list_slice], matchers, ctx, trim_noncode=trim_noncode
        )

    # Make the check tuple
    expected_result = make_result_tuple(
        result_slice=result_slice,
        matcher_keywords=matcher_keywords,
        seg_list=seg_list,
    )

    assert m.matched_segments == expected_result


def test__parser__grammar__base__longest_trimmed_match__adv(seg_list, caplog):
    """Test the _longest_trimmed_match method of the BaseGrammar."""
    bs = KeywordSegment.make("bar")
    fs = KeywordSegment.make("foo")
    matchers = [
        bs,
        fs,
        Sequence(bs, fs),  # This should be the winner.
        OneOf(bs, fs),
        Sequence(bs, fs),  # Another to check we return the first
    ]
    fs = KeywordSegment.make("foo")
    bs = KeywordSegment.make("bar")
    with RootParseContext(dialect=None) as ctx:
        # Matching the first element of the list
        with caplog.at_level(logging.DEBUG, logger="sqluff.parser"):
            match, matcher = BaseGrammar._longest_trimmed_match(seg_list, matchers, ctx)
    # Check we got a match
    assert match
    # Check we got the right one.
    assert matcher is matchers[2]
    # And it matched the first three segments
    assert len(match) == 3


@pytest.mark.parametrize(
    "seg_list_slice,matcher_keywords,result_slice,winning_matcher,pre_match_slice",
    [
        # Basic version, we should find bar first
        (slice(None, None), ["bar", "foo"], slice(None, 1), "bar", None),
        # Look ahead for foo
        (slice(None, None), ["foo"], slice(2, 3), "foo", slice(None, 2)),
    ],
)
def test__parser__grammar__base__look_ahead_match(
    seg_list_slice,
    matcher_keywords,
    result_slice,
    winning_matcher,
    pre_match_slice,
    seg_list,
):
    """Test the _look_ahead_match method of the BaseGrammar."""
    # Make the matcher keywords
    matchers = [KeywordSegment.make(keyword) for keyword in matcher_keywords]
    # Fetch the matching keyword from above by index
    winning_matcher = matchers[matcher_keywords.index(winning_matcher)]

    with RootParseContext(dialect=None) as ctx:
        m = BaseGrammar._look_ahead_match(
            seg_list[seg_list_slice],
            matchers,
            ctx,
        )

    # Check structure of the response.
    assert isinstance(m, tuple)
    assert len(m) == 3
    # Unpack
    result_pre_match, result_match, result_matcher = m

    # Check the right matcher won
    assert result_matcher == winning_matcher

    # Make check tuple for the pre-match section
    if pre_match_slice:
        pre_match_slice = seg_list[pre_match_slice]
    else:
        pre_match_slice = ()
    assert result_pre_match == pre_match_slice

    # Make the check tuple
    expected_result = make_result_tuple(
        result_slice=result_slice,
        matcher_keywords=matcher_keywords,
        seg_list=seg_list,
    )
    assert result_match.matched_segments == expected_result


def test__parser__grammar__base__ephemeral_segment(seg_list):
    """Test the ephemeral features BaseGrammar.

    Normally you cant call .match() on a BaseGrammar, but
    if things are set up right, then it should be possible
    in the case that the ephemeral_name is set.
    """
    g = BaseGrammar(ephemeral_name="TestGrammar")

    with RootParseContext(dialect=None) as ctx:
        m = g.match(seg_list, ctx)
        # Check we get an ephemeral segment
        assert isinstance(m.matched_segments[0], EphemeralSegment)
        chkpoint = m.matched_segments[0]
        # Check it's got the same content.
        assert chkpoint.segments == seg_list


def test__parser__grammar__base__bracket_sensitive_look_ahead_match(
    bracket_seg_list, fresh_ansi_dialect
):
    """Test the _bracket_sensitive_look_ahead_match method of the BaseGrammar."""
    fs = KeywordSegment.make("foo")
    bs = KeywordSegment.make("bar")
    # We need a dialect here to do bracket matching
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        # Basic version, we should find bar first
        pre_section, match, matcher = BaseGrammar._bracket_sensitive_look_ahead_match(
            bracket_seg_list, [fs, bs], ctx
        )
        assert pre_section == ()
        assert matcher == bs
        # NB the middle element is a match object
        assert match.matched_segments == (bs("bar", bracket_seg_list[0].pos_marker),)

        # Look ahead for foo, we should find the one AFTER the brackets, not the
        # on IN the brackets.
        pre_section, match, matcher = BaseGrammar._bracket_sensitive_look_ahead_match(
            bracket_seg_list, [fs], ctx
        )
        # NB: The bracket segments will have been mutated, so we can't directly compare
        assert len(pre_section) == 8
        assert matcher == fs
        # We shouldn't match the whitespace with the keyword
        assert match.matched_segments == (fs("foo", bracket_seg_list[8].pos_marker),)


@pytest.mark.parametrize("allow_gaps", [True, False])
def test__parser__grammar_oneof(seg_list, allow_gaps):
    """Test the OneOf grammar.

    NB: Should behave the same regardless of code_only.

    """
    fs = KeywordSegment.make("foo")
    bs = KeywordSegment.make("bar")
    g = OneOf(fs, bs, allow_gaps=allow_gaps)
    with RootParseContext(dialect=None) as ctx:
        # Check directly
        assert g.match(seg_list, parse_context=ctx).matched_segments == (
            bs("bar", seg_list[0].pos_marker),
        )
        # Check with a bit of whitespace
        assert not g.match(seg_list[1:], parse_context=ctx)


def test__parser__grammar_oneof_exclude(seg_list):
    """Test the OneOf grammar exclude option."""
    fs = KeywordSegment.make("foo")
    bs = KeywordSegment.make("bar")
    g = OneOf(bs, exclude=Sequence(bs, fs))
    with RootParseContext(dialect=None) as ctx:
        # Just against the first alone
        assert g.match(seg_list[:1], parse_context=ctx)
        # Now with the bit to exclude included
        assert not g.match(seg_list, parse_context=ctx)


def test__parser__grammar_oneof_take_longest_match(seg_list):
    """Test that the OneOf grammar takes the longest match."""
    fooRegex = ReSegment.make(r"fo{2}")
    baar = KeywordSegment.make(
        "baar",
    )
    foo = KeywordSegment.make(
        "foo",
    )
    fooBaar = Sequence(
        foo,
        baar,
    )

    # Even if fooRegex comes first, fooBaar
    # is a longer match and should be taken
    g = OneOf(fooRegex, fooBaar)
    with RootParseContext(dialect=None) as ctx:
        assert fooRegex.match(seg_list[2:], parse_context=ctx).matched_segments == (
            fooRegex("foo", seg_list[2].pos_marker),
        )
        assert g.match(seg_list[2:], parse_context=ctx).matched_segments == (
            foo("foo", seg_list[2].pos_marker),
            baar("baar", seg_list[3].pos_marker),
        )


def test__parser__grammar_oneof_take_first(seg_list):
    """Test that the OneOf grammar takes first match in case they are of same length."""
    fooRegex = ReSegment.make(r"fo{2}")
    foo = KeywordSegment.make(
        "foo",
    )

    # Both segments would match "foo"
    # so we test that order matters
    g1 = OneOf(fooRegex, foo)
    g2 = OneOf(foo, fooRegex)
    with RootParseContext(dialect=None) as ctx:
        assert g1.match(seg_list[2:], parse_context=ctx).matched_segments == (
            fooRegex("foo", seg_list[2].pos_marker),
        )
        assert g2.match(seg_list[2:], parse_context=ctx).matched_segments == (
            foo("foo", seg_list[2].pos_marker),
        )


@pytest.mark.parametrize(
    "keyword,match_truthy",
    [
        ("baar", False),
        ("bar", True),
    ],
)
def test__parser__grammar_startswith_a(
    keyword, match_truthy, seg_list, fresh_ansi_dialect, caplog
):
    """Test the StartsWith grammar simply."""
    Keyword = KeywordSegment.make(keyword)
    grammar = StartsWith(Keyword)
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        with caplog.at_level(logging.DEBUG, logger="sqlfluff.parser"):
            m = grammar.match(seg_list, parse_context=ctx)
            assert bool(m) is match_truthy


@pytest.mark.parametrize(
    "include_terminator,match_length",
    [
        (False, 3),
        # NB: In this case we still shouldn't match the trailing whitespace.
        (True, 4),
    ],
)
def test__parser__grammar_startswith_b(
    include_terminator, match_length, seg_list, fresh_ansi_dialect, caplog
):
    """Test the StartsWith grammar with a terminator (included & exluded)."""
    baar = KeywordSegment.make("baar")
    bar = KeywordSegment.make("bar")
    grammar = StartsWith(bar, terminator=baar, include_terminator=include_terminator)
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        with caplog.at_level(logging.DEBUG, logger="sqlfluff.parser"):
            m = grammar.match(seg_list, parse_context=ctx)
            assert len(m) == match_length


def test__parser__grammar_sequence(seg_list, caplog):
    """Test the Sequence grammar."""
    fs = KeywordSegment.make("foo")
    bs = KeywordSegment.make("bar")
    g = Sequence(bs, fs)
    gc = Sequence(bs, fs, allow_gaps=False)
    with RootParseContext(dialect=None) as ctx:
        with caplog.at_level(logging.DEBUG, logger="sqlfluff.parser"):
            # Should be able to match the list using the normal matcher
            logging.info("#### TEST 1")
            m = g.match(seg_list, parse_context=ctx)
            assert m
            assert len(m) == 3
            assert m.matched_segments == (
                bs("bar", seg_list[0].pos_marker),
                seg_list[1],  # This will be the whitespace segment
                fs("foo", seg_list[2].pos_marker),
            )
            # Shouldn't with the allow_gaps matcher
            logging.info("#### TEST 2")
            assert not gc.match(seg_list, parse_context=ctx)
            # Shouldn't match even on the normal one if we don't start at the beginning
            logging.info("#### TEST 2")
            assert not g.match(seg_list[1:], parse_context=ctx)


def test__parser__grammar_sequence_nested(seg_list, caplog):
    """Test the Sequence grammar when nested."""
    fs = KeywordSegment.make("foo")
    bs = KeywordSegment.make("bar")
    bas = KeywordSegment.make("baar")
    g = Sequence(Sequence(bs, fs), bas)
    with RootParseContext(dialect=None) as ctx:
        with caplog.at_level(logging.DEBUG, logger="sqlfluff.parser"):
            # Matching the start of the list shouldn't work
            logging.info("#### TEST 1")
            assert not g.match(seg_list[:2], parse_context=ctx)
            # Matching the whole list should, and the result should be flat
            logging.info("#### TEST 2")
            assert g.match(seg_list, parse_context=ctx).matched_segments == (
                bs("bar", seg_list[0].pos_marker),
                seg_list[1],  # This will be the whitespace segment
                fs("foo", seg_list[2].pos_marker),
                bas("baar", seg_list[3].pos_marker)
                # NB: No whitespace at the end, this shouldn't be consumed.
            )


@pytest.mark.parametrize(
    "token_list,min_delimiters,allow_gaps,allow_trailing,match_len",
    [
        # Basic testing
        (["bar", " \t ", ".", "    ", "bar"], None, True, False, 5),
        (["bar", " \t ", ".", "    ", "bar", "    "], None, True, False, 6),
        # Testing allow_trailing
        (["bar", " \t ", ".", "   "], None, True, False, 0),
        (["bar", " \t ", ".", "   "], None, True, True, 3),
        # Testing the implications of allow_gaps
        (["bar", " \t ", ".", "    ", "bar"], 0, True, False, 5),
        (["bar", " \t ", ".", "    ", "bar"], 0, False, False, 1),
        (["bar", " \t ", ".", "    ", "bar"], 1, True, False, 5),
        (["bar", " \t ", ".", "    ", "bar"], 1, False, False, 0),
        (["bar", ".", "bar"], None, True, False, 3),
        (["bar", ".", "bar"], None, False, False, 3),
        (["bar", ".", "bar"], 1, True, False, 3),
        (["bar", ".", "bar"], 1, False, False, 3),
        # Check we still succeed with something trailing right on the end.
        (["bar", ".", "bar", "foo"], 1, False, False, 3),
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
    seg_list = generate_test_segments(token_list)
    g = Delimited(
        KeywordSegment.make("bar"),
        delimiter=KeywordSegment.make(".", name="dot"),
        allow_gaps=allow_gaps,
        allow_trailing=allow_trailing,
        min_delimiters=min_delimiters,
    )
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        with caplog.at_level(logging.DEBUG, logger="sqlfluff.parser"):
            # Matching with whitespace shouldn't match if we need at least one delimiter
            m = g.match(seg_list, parse_context=ctx)
            assert len(m) == match_len


@pytest.mark.parametrize(
    "keyword,enforce_ws,slice_len",
    [
        # Basic testing
        ("foo", False, 1),
        # Greedy matching until the first item should return none
        ("bar", False, 0),
        # Greedy matching up to baar should return bar, foo...
        ("baar", False, 3),
        # ... except if whitespace is required to preceed it
        ("baar", True, 5),
    ],
)
def test__parser__grammar_greedyuntil(
    keyword, seg_list, enforce_ws, slice_len, fresh_ansi_dialect
):
    """Test the GreedyUntil grammar."""
    grammar = GreedyUntil(
        KeywordSegment.make(keyword),
        enforce_whitespace_preceeding_terminator=enforce_ws,
    )
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        assert (
            grammar.match(seg_list, parse_context=ctx).matched_segments
            == seg_list[:slice_len]
        )


def test__parser__grammar_greedyuntil_bracketed(bracket_seg_list, fresh_ansi_dialect):
    """Test the GreedyUntil grammar with brackets."""
    fs = KeywordSegment.make("foo")
    g = GreedyUntil(fs)
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        # Check that we can make it past the brackets
        assert len(g.match(bracket_seg_list, parse_context=ctx)) == 7


def test__parser__grammar_anything(seg_list, fresh_ansi_dialect):
    """Test the Anything grammar."""
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        assert Anything().match(seg_list, parse_context=ctx)


def test__parser__grammar_nothing(seg_list, fresh_ansi_dialect):
    """Test the Nothing grammar."""
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        assert not Nothing().match(seg_list, parse_context=ctx)


def test__parser__grammar_noncode(seg_list, fresh_ansi_dialect):
    """Test the NonCodeMatcher."""
    with RootParseContext(dialect=fresh_ansi_dialect) as ctx:
        m = NonCodeMatcher().match(seg_list[1:], parse_context=ctx)
    # We should match one and only one segment
    assert len(m) == 1
