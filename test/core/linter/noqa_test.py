"""The Test file for the linter class."""

from typing import List
import pytest

from sqlfluff.core import Linter, FluffConfig
from sqlfluff.core.errors import (
    SQLBaseError,
    SQLParseError,
)
from sqlfluff.core.linter import NoQaDirective, IgnoreMask


# noqa tests require a rule_set, therefore we construct dummy rule set for glob matching.
dummy_rule_map = Linter().get_rulepack().reference_map


class DummyLintError(SQLBaseError):
    """Fake lint error used by tests, similar to SQLLintError."""

    def __init__(self, line_no: int, code: str = "LT01"):
        self._code = code
        super().__init__(line_no=line_no)


def test__linter__raises_malformed_noqa():
    """A badly formatted noqa gets raised as a parsing error."""
    lntr = Linter(dialect="ansi")
    result = lntr.lint_string_wrapped("select 1 --noqa missing semicolon")

    with pytest.raises(SQLParseError):
        result.check_tuples()


@pytest.mark.parametrize(
    "input,expected",
    [
        ("", None),
        ("noqa", NoQaDirective(0, None, None)),
        ("noqa?", SQLParseError),
        ("noqa:", NoQaDirective(0, None, None)),
        ("noqa:LT01,LT02", NoQaDirective(0, ("LT01", "LT02"), None)),
        ("noqa: enable=LT01", NoQaDirective(0, ("LT01",), "enable")),
        ("noqa: disable=CP01", NoQaDirective(0, ("CP01",), "disable")),
        ("noqa: disable=all", NoQaDirective(0, None, "disable")),
        ("noqa: disable", SQLParseError),
        (
            "Inline comment before inline ignore -- noqa:LT01,LT02",
            NoQaDirective(0, ("LT01", "LT02"), None),
        ),
        # Test selection with rule globs
        (
            "noqa:L04*",
            NoQaDirective(
                0,
                (
                    "AM04",  # L044 is an alias of AM04
                    "CP04",  # L040 is an alias of CP04
                    "CV04",  # L047 is an alias of CV04
                    "CV05",  # L049 is an alias of CV05
                    "JJ01",  # L046 is an alias of JJ01
                    "LT01",  # L048 is an alias of LT01
                    "LT10",  # L041 is an alias of LT10
                    "ST02",  # L043 is an alias of ST02
                    "ST03",  # L045 is an alias of ST03
                    "ST05",  # L042 is an alias of ST05
                ),
                None,
            ),
        ),
        # Test selection with aliases.
        (
            "noqa:L002",
            NoQaDirective(0, ("LT02",), None),
        ),
        # Test selection with alias globs.
        (
            "noqa:L00*",
            NoQaDirective(
                0,
                ("LT01", "LT02", "LT03", "LT12"),
                None,
            ),
        ),
        # Test selection with names.
        (
            "noqa:capitalisation.keywords",
            NoQaDirective(0, ("CP01",), None),
        ),
        # Test selection with groups.
        (
            "noqa:capitalisation",
            NoQaDirective(0, ("CP01", "CP02", "CP03", "CP04", "CP05"), None),
        ),
    ],
)
def test_parse_noqa(input, expected):
    """Test correct of "noqa" comments."""
    result = IgnoreMask._parse_noqa(input, 0, reference_map=dummy_rule_map)
    if not isinstance(expected, type):
        assert result == expected
    else:
        # With exceptions, just check the type, not the contents.
        assert isinstance(result, expected)


def test_parse_noqa_no_dups():
    """Test overlapping glob expansions don't return duplicate rules in noqa."""
    result = IgnoreMask._parse_noqa(
        comment="noqa:L0*5,L01*", line_no=0, reference_map=dummy_rule_map
    )
    assert len(result.rules) == len(set(result.rules))


@pytest.mark.parametrize(
    "noqa,violations,expected",
    [
        [
            [],
            [DummyLintError(1)],
            [
                0,
            ],
        ],
        [
            [dict(comment="noqa: LT01", line_no=1)],
            [DummyLintError(1)],
            [],
        ],
        [
            [dict(comment="noqa: LT01", line_no=2)],
            [DummyLintError(1)],
            [0],
        ],
        [
            [dict(comment="noqa: LT02", line_no=1)],
            [DummyLintError(1)],
            [0],
        ],
        [
            [dict(comment="noqa: enable=LT01", line_no=1)],
            [DummyLintError(1)],
            [0],
        ],
        [
            [dict(comment="noqa: disable=LT01", line_no=1)],
            [DummyLintError(1)],
            [],
        ],
        [
            [
                dict(comment="noqa: disable=LT01", line_no=2),
                dict(comment="noqa: enable=LT01", line_no=4),
            ],
            [DummyLintError(1)],
            [0],
        ],
        [
            [
                dict(comment="noqa: disable=LT01", line_no=2),
                dict(comment="noqa: enable=LT01", line_no=4),
            ],
            [DummyLintError(2)],
            [],
        ],
        [
            [
                dict(comment="noqa: disable=LT01", line_no=2),
                dict(comment="noqa: enable=LT01", line_no=4),
            ],
            [DummyLintError(3)],
            [],
        ],
        [
            [
                dict(comment="noqa: disable=LT01", line_no=2),
                dict(comment="noqa: enable=LT01", line_no=4),
            ],
            [DummyLintError(4)],
            [0],
        ],
        [
            [
                dict(comment="noqa: disable=all", line_no=2),
                dict(comment="noqa: enable=all", line_no=4),
            ],
            [DummyLintError(1)],
            [0],
        ],
        [
            [
                dict(comment="noqa: disable=all", line_no=2),
                dict(comment="noqa: enable=all", line_no=4),
            ],
            [DummyLintError(2)],
            [],
        ],
        [
            [
                dict(comment="noqa: disable=all", line_no=2),
                dict(comment="noqa: enable=all", line_no=4),
            ],
            [DummyLintError(3)],
            [],
        ],
        [
            [
                dict(comment="noqa: disable=all", line_no=2),
                dict(comment="noqa: enable=all", line_no=4),
            ],
            [DummyLintError(4)],
            [0],
        ],
        [
            [
                dict(comment="noqa: disable=LT01", line_no=2),
                dict(comment="noqa: enable=all", line_no=4),
            ],
            [
                DummyLintError(2, code="LT01"),
                DummyLintError(2, code="LT02"),
                DummyLintError(4, code="LT01"),
                DummyLintError(4, code="LT02"),
            ],
            [1, 2, 3],
        ],
        [
            [
                dict(comment="noqa: disable=all", line_no=2),
                dict(comment="noqa: enable=LT01", line_no=4),
            ],
            [
                DummyLintError(2, code="LT01"),
                DummyLintError(2, code="LT02"),
                DummyLintError(4, code="LT01"),
                DummyLintError(4, code="LT02"),
            ],
            [2],
        ],
        [
            [
                dict(
                    comment="Inline comment before inline ignore -- noqa: LT02",
                    line_no=1,
                )
            ],
            [DummyLintError(1)],
            [0],
        ],
        [
            [
                dict(
                    comment="Inline comment before inline ignore -- noqa: LT02",
                    line_no=1,
                ),
                dict(
                    comment="Inline comment before inline ignore -- noqa: LT02",
                    line_no=2,
                ),
            ],
            [
                DummyLintError(1),
                DummyLintError(2),
            ],
            [0, 1],
        ],
        [
            [
                dict(
                    comment="Inline comment before inline ignore -- noqa: L01*",
                    line_no=1,
                ),
            ],
            [
                DummyLintError(1),
            ],
            [0],
        ],
    ],
    ids=[
        "1_violation_no_ignore",
        "1_violation_ignore_specific_line",
        "1_violation_ignore_different_specific_line",
        "1_violation_ignore_different_specific_rule",
        "1_violation_ignore_enable_this_range",
        "1_violation_ignore_disable_this_range",
        "1_violation_line_1_ignore_disable_specific_2_3",
        "1_violation_line_2_ignore_disable_specific_2_3",
        "1_violation_line_3_ignore_disable_specific_2_3",
        "1_violation_line_4_ignore_disable_specific_2_3",
        "1_violation_line_1_ignore_disable_all_2_3",
        "1_violation_line_2_ignore_disable_all_2_3",
        "1_violation_line_3_ignore_disable_all_2_3",
        "1_violation_line_4_ignore_disable_all_2_3",
        "4_violations_two_types_disable_specific_enable_all",
        "4_violations_two_types_disable_all_enable_specific",
        "1_violations_comment_inline_ignore",
        "2_violations_comment_inline_ignore",
        "1_violations_comment_inline_glob_ignore",
    ],
)
def test_linted_file_ignore_masked_violations(
    noqa: dict, violations: List[SQLBaseError], expected
):
    """Test that _ignore_masked_violations() correctly filters violations."""
    ignore_mask = [
        IgnoreMask._parse_noqa(reference_map=dummy_rule_map, **c) for c in noqa
    ]
    result = IgnoreMask(ignore_mask).ignore_masked_violations(violations)
    expected_violations = [v for i, v in enumerate(violations) if i in expected]
    assert expected_violations == result


def test_linter_noqa():
    """Test "noqa" feature at the higher "Linter" level."""
    lntr = Linter(
        config=FluffConfig(
            overrides={
                "dialect": "bigquery",  # Use bigquery to allow hash comments.
                "rules": "AL02, LT04",
            }
        )
    )
    sql = """
    SELECT
        col_a a,
        col_b b, --noqa: disable=AL02
        col_c c,
        col_d d, --noqa: enable=AL02
        col_e e,
        col_f f,
        col_g g,  --noqa
        col_h h,
        col_i i, --noqa:AL02
        col_j j,
        col_k k, --noqa:AL03
        col_l l,
        col_m m,
        col_n n, --noqa: disable=all
        col_o o,
        col_p p, --noqa: enable=all
        col_q q, --Inline comment --noqa: AL02
        col_r r, /* Block comment */ --noqa: AL02
        col_s s # hash comment --noqa: AL02
        -- We trigger both AL02 (implicit aliasing)
        -- and LT04 (leading commas) here to
        -- test glob ignoring of multiple rules.
        , col_t t --noqa: L01*
        , col_u u -- Some comment --noqa: L01*
        , col_v v -- We can ignore both AL02 and LT04 -- noqa: L01[29]
    FROM foo
        """
    result = lntr.lint_string(sql)
    violations = result.get_violations()
    assert {3, 6, 7, 8, 10, 12, 13, 14, 15, 18} == {v.line_no for v in violations}


def test_linter_noqa_with_templating():
    """Similar to test_linter_noqa, but uses templating (Jinja)."""
    lntr = Linter(
        config=FluffConfig(
            overrides={
                "dialect": "bigquery",  # Use bigquery to allow hash comments.
                "templater": "jinja",
                "rules": "LT05",
            }
        )
    )
    sql = "\n"
    '"{%- set a_var = ["1", "2"] -%}\n'
    "SELECT\n"
    "  this_is_just_a_very_long_line_for_demonstration_purposes_of_a_bug_involving_"
    "templated_sql_files, --noqa: LT05\n"
    "  this_is_not_so_big a, --Inline comment --noqa: AL02\n"
    "  this_is_not_so_big b, /* Block comment */ --noqa: AL02\n"
    "  this_is_not_so_big c, # hash comment --noqa: AL02\n"
    "  this_is_just_a_very_long_line_for_demonstration_purposes_of_a_bug_involving_"
    "templated_sql_files, --noqa: L01*\n"
    "FROM\n"
    "  a_table\n"
    "    "
    result = lntr.lint_string(sql)
    assert not result.get_violations()


def test_linter_noqa_template_errors():
    """Similar to test_linter_noqa, but uses templating (Jinja)."""
    lntr = Linter(
        config=FluffConfig(
            overrides={
                "templater": "jinja",
                "dialect": "ansi",
            }
        )
    )
    sql = """select * --noqa: TMP
from raw
where
    balance_date >= {{ execution_date - macros.timedelta() }}  --noqa: TMP
"""
    result = lntr.lint_string(sql)
    assert not result.get_violations()


def test_linter_noqa_prs():
    """Test "noqa" feature to ignore PRS at the higher "Linter" level."""
    lntr = Linter(dialect="ansi")
    sql = "SELEC * FROM foo -- noqa: PRS\n"
    result = lntr.lint_string(sql)
    violations = result.get_violations()
    assert not violations


def test_linter_noqa_tmp():
    """Test "noqa" feature to ignore TMP at the higher "Linter" level."""
    lntr = Linter(
        config=FluffConfig(
            overrides={
                "exclude_rules": "LT13",
                "dialect": "ansi",
            }
        )
    )
    sql = """
SELECT {{ col_a }} AS a -- noqa: TMP,PRS
FROM foo;
"""
    result = lntr.lint_string(sql)
    print(result.tree.stringify())
    violations = result.get_violations()
    assert not violations


def test_linter_noqa_disable():
    """Test "noqa" comments can be disabled via the config."""
    lntr_noqa_enabled = Linter(
        config=FluffConfig(
            overrides={
                "rules": "AL02",
                "dialect": "ansi",
            }
        )
    )
    lntr_noqa_disabled = Linter(
        config=FluffConfig(
            overrides={
                "disable_noqa": True,
                "rules": "AL02",
                "dialect": "ansi",
            }
        )
    )
    # This query raises AL02, but it is being suppressed by the inline noqa comment.
    # We can ignore this comment by setting disable_noqa = True in the config
    # or by using the --disable-noqa flag in the CLI.
    sql = """
    SELECT col_a a --noqa: AL02
    FROM foo
    """

    # Verify that noqa works as expected with disable_noqa = False (default).
    result_noqa_enabled = lntr_noqa_enabled.lint_string(sql)
    violations_noqa_enabled = result_noqa_enabled.get_violations()
    assert len(violations_noqa_enabled) == 0

    # Verify that noqa comment is ignored with disable_noqa = True.
    result_noqa_disabled = lntr_noqa_disabled.lint_string(sql)
    violations_noqa_disabled = result_noqa_disabled.get_violations()
    assert len(violations_noqa_disabled) == 1
    assert violations_noqa_disabled[0].rule.code == "AL02"
