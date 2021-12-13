"""Tests for templaters."""
import pytest

from sqlfluff.core import FluffConfig
from sqlfluff.core.templaters import PlaceholderTemplater
from sqlfluff.core.errors import SQLTemplaterError
from sqlfluff.core.templaters.placeholder import AUTOFILL_PARAMS


def test__templater_raw():
    """Test the templaters when nothing has to be replaced."""
    t = PlaceholderTemplater(override_context=dict(param_style="colon"))
    instr = "SELECT * FROM {{blah}} WHERE %(gnepr)s OR e~':'"
    outstr, _ = t.process(in_str=instr, fname="test")
    assert str(outstr) == instr


@pytest.mark.parametrize(
    "instr, param_style, expected_outstr, values",
    [
        (
            "SELECT * FROM f, o, o WHERE a < 10\n\n",
            "colon",
            "SELECT * FROM f, o, o WHERE a < 10\n\n",
            dict(
                unused=7777,
            ),
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = :user_id AND date > :start_date
            """,
            "colon",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = 42 AND date > '2021-10-01'
            """,
            dict(
                user_id="42",
                start_date="'2021-10-01'",
                city_ids="(1, 2, 3, 45)",
            ),
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = :user_id AND date > :start_date""",
            "colon",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = 42 AND date > '2021-10-01'""",
            dict(
                user_id="42",
                start_date="'2021-10-01'",
                city_ids="(1, 2, 3, 45)",
            ),
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN :city_ids
            AND date > '2020-10-01'
            """,
            "colon",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN (1, 2, 3, 45)
            AND date > '2020-10-01'
            """,
            dict(
                user_id="42",
                start_date="'2021-10-01'",
                city_ids="(1, 2, 3, 45)",
            ),
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN ?
            AND date > ?
            """,
            "question_mark",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN (1, 2, 3, 45)
            AND date > '2020-10-01'
            """,
            {
                "1": "(1, 2, 3, 45)",
                "2": "'2020-10-01'",
            },
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN :1
            AND date > :45
            """,
            "numeric_colon",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN (1, 2, 3, 45)
            AND date > '2020-10-01'
            """,
            {
                "1": "(1, 2, 3, 45)",
                "45": "'2020-10-01'",
            },
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN %(city_id)s
            AND date > %(date)s
            """,
            "pyformat",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN (1, 2, 3, 45)
            AND date > '2020-10-01'
            """,
            dict(
                city_id="(1, 2, 3, 45)",
                date="'2020-10-01'",
            ),
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN $city_id
            AND date > $date
            """,
            "dollar",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN (1, 2, 3, 45)
            AND date > '2020-10-01'
            """,
            dict(
                city_id="(1, 2, 3, 45)",
                date="'2020-10-01'",
            ),
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN $12
            AND date > $90
            """,
            "numeric_dollar",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN (1, 2, 3, 45)
            AND date > '2020-10-01'
            """,
            {
                "12": "(1, 2, 3, 45)",
                "90": "'2020-10-01'",
            },
        ),
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN %s
            AND date > %s
            """,
            "percent",
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE (city_id) IN (1, 2, 3, 45)
            AND date > '2020-10-01'
            """,
            {
                "1": "(1, 2, 3, 45)",
                "2": "'2020-10-01'",
            },
        ),
        (
            """
            USE DATABASE &{env}_MARKETING;
            USE SCHEMA &&EMEA;
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = &user_id AND date > &{start_date}
            """,
            "ampersand",
            """
            USE DATABASE PRD_MARKETING;
            USE SCHEMA &&EMEA;
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = 42 AND date > '2021-10-01'
            """,
            dict(
                env="PRD",
                user_id="42",
                start_date="'2021-10-01'",
            ),
        ),
    ],
    ids=[
        "no_changes",
        "colon_simple_substitution",
        "colon_accept_block_at_end",
        "colon_tuple_substitution",
        "question_mark",
        "numeric_colon",
        "pyformat",
        "dollar",
        "numeric_dollar",
        "percent",
        "ampersand",
    ],
)
def test__templater_param_style(instr, expected_outstr, param_style, values):
    """Test different param_style templating."""
    t = PlaceholderTemplater(override_context={**values, "param_style": param_style})
    outstr, _ = t.process(in_str=instr, fname="test", config=FluffConfig())
    assert str(outstr) == expected_outstr


def test__templater_custom_regex():
    """Test custom regex templating."""
    t = PlaceholderTemplater(
        override_context=dict(param_regex="__(?P<param_name>[\\w_]+)__", my_name="john")
    )
    outstr, _ = t.process(
        in_str="SELECT bla FROM blob WHERE id = __my_name__",
        fname="test",
        config=FluffConfig(),
    )
    assert str(outstr) == "SELECT bla FROM blob WHERE id = john"


@pytest.mark.parametrize(
    "instr, expected_outstr",
    [
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param AND explicit_param = @explicit_param",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['string']} AND explicit_param = explicit_param",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param IS @missing_param::boolean",
            f"SELECT bla FROM blob WHERE missing_param IS {AUTOFILL_PARAMS['boolean']}",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param::integer",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['integer']}",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param::float",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['float']}",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param::date",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['date']}",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param::integer[]",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['integer_array']}",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param::text[]",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['text_array']}",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param::boolean[]",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['boolean_array']}",
        ),
        (
            "SELECT bla FROM blob WHERE missing_param = @missing_param::float[]",
            f"SELECT bla FROM blob WHERE missing_param = {AUTOFILL_PARAMS['float_array']}",
        ),
    ],
    ids=[
        "ignore_explicit_param_and_autofill_missing_untyped_param",
        "autofill_missing_params_boolean",
        "autofill_missing_params_integer",
        "autofill_missing_params_float",
        "autofill_missing_params_date",
        "autofill_missing_params_integer_array",
        "autofill_missing_params_string_array",
        "autofill_missing_params_boolean_array",
        "autofill_missing_params_float_array",
    ],
)
def test__templater_custom_regex_autofill_params_parametrized(instr, expected_outstr):
    """Test custom regex param autofill."""
    t = PlaceholderTemplater(
        override_context=dict(
            param_regex=r"@(?P<param_name>[\w_]+)(::(?P<param_type>[\w_\[\]]+))?",
            autofill_missing_params=True,
            explicit_param="explicit_param",
        )
    )
    outstr, _ = t.process(
        in_str=instr,
        fname="test",
        config=FluffConfig(),
    )
    assert str(outstr) == expected_outstr


def test__templater_exception():
    """Test the exception raised when variables are missing."""
    t = PlaceholderTemplater(override_context=dict(name="'john'", param_style="colon"))
    instr = "SELECT name FROM table WHERE user_id = :user_id"
    with pytest.raises(
        SQLTemplaterError, match=r"Failure in placeholder templating: 'user_id'"
    ):
        t.process(in_str=instr, fname="test")


def test__templater_setup():
    """Test the exception raised when config is incomplete or ambiguous."""
    t = PlaceholderTemplater(override_context=dict(name="'john'"))
    with pytest.raises(
        ValueError,
        match=r"No param_regex nor param_style was provided to the placeholder templater",
    ):
        t.process(in_str="SELECT 2+2", fname="test")

    t = PlaceholderTemplater(
        override_context=dict(param_style="bla", param_regex="bli")
    )
    with pytest.raises(
        ValueError,
        match=r"Either param_style or param_regex must be provided, not both",
    ):
        t.process(in_str="SELECT 2+2", fname="test")


def test__templater_styles():
    """Test the exception raised when parameter style is unknown."""
    t = PlaceholderTemplater(override_context=dict(param_style="pperccent"))
    with pytest.raises(ValueError, match=r"Unknown param_style"):
        t.process(in_str="SELECT 2+2", fname="test")
