"""Fixtures for dbt templating tests."""

from sqlfluff.core.templaters import DbtTemplater
import pytest
import os


DBT_FLUFF_CONFIG = {
    "core": {
        "templater": "dbt",
        "dialect": "postgres",
    },
    "templater": {
        "dbt": {
            "profiles_dir": "../dbt",
        },
    },
}


@pytest.fixture()
def dbt_templater():
    """Returns an instance of the DbtTemplater."""
    return DbtTemplater()


@pytest.fixture()
def in_dbt_project_dir():
    """A wrapper to chdir into the dbt_project fixture and back to cwd at the end of the test."""
    try:
        pre_test_dir = os.getcwd()
        os.chdir("test/fixtures/dbt_project")
        yield  # test runs here
    finally:
        os.chdir(pre_test_dir)
