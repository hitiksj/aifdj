"""The Test file for the linter class."""

import pytest
from unittest.mock import patch

from sqlfluff.core import Linter, FluffConfig
from sqlfluff.core.errors import SQLLintError, SQLParseError
from sqlfluff.core.linter import LintingResult


def normalise_paths(paths):
    """Test normalising paths.

    NB Paths on difference platforms might look different, so this
    makes them comparable.
    """
    return {pth.replace("/", ".").replace("\\", ".") for pth in paths}


def test__linter__path_from_paths__dir():
    """Test extracting paths from directories."""
    lntr = Linter()
    paths = lntr.paths_from_path("test/fixtures/lexer")
    assert normalise_paths(paths) == {
        "test.fixtures.lexer.block_comment.sql",
        "test.fixtures.lexer.inline_comment.sql",
        "test.fixtures.lexer.basic.sql",
    }


def test__linter__path_from_paths__file():
    """Test extracting paths from a file path."""
    lntr = Linter()
    paths = lntr.paths_from_path("test/fixtures/linter/indentation_errors.sql")
    assert normalise_paths(paths) == {"test.fixtures.linter.indentation_errors.sql"}


def test__linter__path_from_paths__not_exist():
    """Test extracting paths from a file path."""
    lntr = Linter()
    with pytest.raises(IOError):
        lntr.paths_from_path("asflekjfhsakuefhse")


def test__linter__path_from_paths__not_exist_ignore():
    """Test extracting paths from a file path."""
    lntr = Linter()
    paths = lntr.paths_from_path("asflekjfhsakuefhse", ignore_non_existent_files=True)
    assert len(paths) == 0


def test__linter__path_from_paths__explicit_ignore():
    """Test ignoring files that were passed explicitly."""
    lntr = Linter(config=FluffConfig())
    paths = lntr.paths_from_path(
        "test/fixtures/linter/sqlfluffignore/path_a/query_a.sql",
        ignore_non_existent_files=True,
        ignore_files=True,
        working_path="test/fixtures/linter/sqlfluffignore/",
    )
    assert len(paths) == 0


def test__linter__path_from_paths__dot():
    """Test extracting paths from a dot."""
    lntr = Linter()
    paths = lntr.paths_from_path(".")
    # Use set theory to check that we get AT LEAST these files
    assert normalise_paths(paths) >= {
        "test.fixtures.lexer.block_comment.sql",
        "test.fixtures.lexer.inline_comment.sql",
        "test.fixtures.lexer.basic.sql",
    }


@pytest.mark.parametrize(
    "path",
    [
        "test/fixtures/linter/sqlfluffignore",
        "test/fixtures/linter/sqlfluffignore/",
        "test/fixtures/linter/sqlfluffignore/.",
    ],
)
def test__linter__path_from_paths__ignore(path):
    """Test extracting paths from a dot."""
    lntr = Linter()
    paths = lntr.paths_from_path(path)
    # We should only get query_b, because of the sqlfluffignore files.
    assert normalise_paths(paths) == {
        "test.fixtures.linter.sqlfluffignore.path_b.query_b.sql"
    }


@pytest.mark.parametrize(
    "path",
    [
        "test/fixtures/linter/indentation_errors.sql",
        "test/fixtures/linter/whitespace_errors.sql",
    ],
)
def test__linter__lint_string_vs_file(path):
    """Test the linter finds the same things on strings and files."""
    with open(path, "r") as f:
        sql_str = f.read()
    lntr = Linter()
    assert (
        lntr.lint_string(sql_str).check_tuples() == lntr.lint_path(path).check_tuples()
    )


@pytest.mark.parametrize(
    "rules,num_violations", [(None, 7), ("L010", 2), (("L001", "L009", "L031"), 2)]
)
def test__linter__get_violations_filter_rules(rules, num_violations):
    """Test filtering violations by which rules were violated."""
    lntr = Linter()
    lint_result = lntr.lint_string("select a, b FROM tbl c order BY d")

    assert len(lint_result.get_violations(rules=rules)) == num_violations


def test__linter__linting_result__sum_dicts():
    """Test the summing of dictionaries in the linter."""
    lr = LintingResult()
    i = {}
    a = dict(a=3, b=123, f=876.321)
    b = dict(a=19, b=321.0, g=23478)
    r = dict(a=22, b=444.0, f=876.321, g=23478)
    assert lr.sum_dicts(a, b) == r
    # Check the identity too
    assert lr.sum_dicts(r, i) == r


def test__linter__linting_result__combine_dicts():
    """Test the combination of dictionaries in the linter."""
    lr = LintingResult()
    a = dict(a=3, b=123, f=876.321)
    b = dict(h=19, i=321.0, j=23478)
    r = dict(z=22)
    assert lr.combine_dicts(a, b, r) == dict(
        a=3, b=123, f=876.321, h=19, i=321.0, j=23478, z=22
    )


@pytest.mark.parametrize("by_path,result_type", [(False, list), (True, dict)])
def test__linter__linting_result_check_tuples_by_path(by_path, result_type):
    """Test that a LintingResult can partition violations by the source files."""
    lntr = Linter()
    result = lntr.lint_paths(
        [
            "test/fixtures/linter/comma_errors.sql",
            "test/fixtures/linter/whitespace_errors.sql",
        ]
    )
    check_tuples = result.check_tuples(by_path=by_path)
    isinstance(check_tuples, result_type)


def test__linter__linting_result_get_violations():
    """Test that we can get violations from a LintingResult."""
    lntr = Linter()
    result = lntr.lint_paths(
        [
            "test/fixtures/linter/comma_errors.sql",
            "test/fixtures/linter/whitespace_errors.sql",
        ]
    )

    all([type(v) == SQLLintError for v in result.get_violations()])


@patch("sqlfluff.core.linter.linter_logger")
@patch("sqlfluff.core.Linter.lint_string")
def test__linter__linting_unexpected_error_handled_gracefully(
    patched_lint_string, patched_logger
):
    """Test that an unexpected internal error is handled gracefully and returns the issue-surfacing file."""
    patched_lint_string.side_effect = Exception("Something unexpected happened")
    lntr = Linter()
    lntr.lint_paths(["test/fixtures/linter/passing.sql"])
    assert (
        "Unable to lint test/fixtures/linter/passing.sql due to an internal error."
        in patched_logger.warning.call_args[0][0]
        and "Exception: Something unexpected happened"
        in patched_logger.warning.call_args[0][0]
    )


def test__linter__raises_malformed_noqa():
    """A badly formatted noqa gets raised as a parsing error."""
    lntr = Linter()
    result = lntr.lint_string_wrapped("select 1 --noqa missing semicolon")

    with pytest.raises(SQLParseError):
        result.check_tuples()


def test__linter__empty_file():
    """Test linter behaves nicely with an empty string."""
    lntr = Linter()
    # Make sure no exceptions raised and no violations found in empty file.
    parsed = lntr.parse_string("")
    assert not parsed.violations
