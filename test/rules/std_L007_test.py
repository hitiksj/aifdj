"""Tests the python routines within L007."""

import sqlfluff
from sqlfluff.core.config import FluffConfig
from sqlfluff.core import Linter

from sqlfluff.rules.L007 import after_description, before_description


def test__rules__std_L007_default():
    """Verify that L007 returns the correct error message for default (trailing)."""
    sql = """
        SELECT
            a,
            b
        FROM foo
        WHERE
            a = 1 AND
            b = 2
    """
    result = sqlfluff.lint(sql)
    assert "L007" in [r["code"] for r in result]
    assert after_description in [r["description"] for r in result]


def test__rules__std_L007_leading():
    """Verify correct error message when leading is used."""
    sql = """
        SELECT
            a,
            b
        FROM foo
        WHERE
            a = 1 AND
            b = 2
    """
    config = FluffConfig(
        configs={"layout": {"type": {"binary_operator": {"line_position": "leading"}}}},
        overrides={"dialect": "ansi"},
    )
    # The sqlfluff.lint API doesn't allow us to pass config so need to do what it does
    linter = Linter(config=config)
    result_records = linter.lint_string_wrapped(sql).as_records()
    result = result_records[0]["violations"]
    assert "L007" in [r["code"] for r in result]
    assert after_description in [r["description"] for r in result]


def test__rules__std_L007_trailing():
    """Verify correct error message when trailing is used."""
    sql = """
        SELECT
            a,
            b
        FROM foo
        WHERE
            a = 1
            AND b = 2
    """
    config = FluffConfig(
        configs={
            "layout": {"type": {"binary_operator": {"line_position": "trailing"}}}
        },
        overrides={"dialect": "ansi"},
    )
    # The sqlfluff.lint API doesn't allow us to pass config so need to do what it does
    linter = Linter(config=config)
    result_records = linter.lint_string_wrapped(sql).as_records()
    result = result_records[0]["violations"]
    assert "L007" in [r["code"] for r in result]
    assert before_description in [r["description"] for r in result]
