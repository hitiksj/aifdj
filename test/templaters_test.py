"""Tests for templaters."""

import pytest

from sqlfluff.templaters import (
    RawTemplateInterface,
    templater_selector,
    PythonTemplateInterface,
    JinjaTemplateInterface,
)
from sqlfluff.linter import Linter
from sqlfluff.config import FluffConfig
from sqlfluff.errors import SQLTemplaterError


def test__templater_selection():
    """Test template selection by name."""
    assert templater_selector().__class__ is JinjaTemplateInterface
    assert templater_selector("raw").__class__ is RawTemplateInterface
    assert templater_selector("python").__class__ is PythonTemplateInterface
    assert templater_selector("jinja").__class__ is JinjaTemplateInterface
    with pytest.raises(ValueError):
        templater_selector("afefhlsakufe")


def test__templater_raw():
    """Test the raw templater."""
    t = RawTemplateInterface()
    instr = "SELECT * FROM {{blah}}"
    outstr, _ = t.process(instr)
    assert instr == outstr


PYTHON_STRING = "SELECT * FROM {blah}"


def test__templater_python():
    """Test the python templater."""
    t = PythonTemplateInterface(override_context=dict(blah="foo"))
    instr = PYTHON_STRING
    outstr, _ = t.process(instr)
    assert outstr == "SELECT * FROM foo"


def test__templater_python_error():
    """Test error handling in the python templater."""
    t = PythonTemplateInterface(override_context=dict(noblah="foo"))
    instr = PYTHON_STRING
    with pytest.raises(SQLTemplaterError):
        t.process(instr)


JINJA_STRING = "SELECT * FROM {% for c in blah %}{{c}}{% if not loop.last %}, {% endif %}{% endfor %} WHERE {{condition}}\n\n"


def test__templater_jinja():
    """Test jinja templating and the treatment of whitespace."""
    t = JinjaTemplateInterface(override_context=dict(blah="foo", condition="a < 10"))
    instr = JINJA_STRING
    outstr, _ = t.process(instr, config=FluffConfig())
    assert outstr == "SELECT * FROM f, o, o WHERE a < 10\n\n"


def test__templater_jinja_error():
    """Test error handling in the jinja templater."""
    t = JinjaTemplateInterface(override_context=dict(blah="foo"))
    instr = JINJA_STRING
    outstr, vs = t.process(instr, config=FluffConfig())
    assert outstr == "SELECT * FROM f, o, o WHERE \n\n"
    # Check we have violations.
    assert len(vs) > 0


def test__templater_jinja_error_catatrophic():
    """Test error handling in the jinja templater."""
    t = JinjaTemplateInterface(override_context=dict(blah=7))
    instr = JINJA_STRING
    outstr, vs = t.process(instr, config=FluffConfig())
    assert not outstr
    assert len(vs) > 0


def assert_structure(yaml_loader, path, code_only=True):
    """Check that a parsed sql file matches the yaml file with the same name."""
    lntr = Linter(config=FluffConfig())
    p = list(lntr.parse_path(path + ".sql"))
    parsed = p[0][0]
    if parsed is None:
        print(p)
        raise RuntimeError(p[0][1])
    # Whitespace is important here to test how that's treated
    tpl = parsed.to_tuple(code_only=code_only, show_raw=True)
    # Check nothing unparsable
    if "unparsable" in parsed.type_set():
        print(parsed.stringify())
        raise ValueError("Input file is contains unparsable.")
    expected = yaml_loader(path + ".yml")
    assert tpl == expected


@pytest.mark.parametrize(
    "subpath,code_only",
    [
        # Config Scalar
        ("jinja_a/jinja", True),
        # Macros
        ("jinja_b/jinja", False),
        # dbt builting
        ("jinja_c_dbt/dbt_builtins", True),
        # do directive
        ("jinja_e/jinja", True),
        # case sensitivity and python literals
        ("jinja_f/jinja", True),
        # Macro loading from a folder
        ("jinja_g_macros/jinja", True),
    ],
)
def test__templater_full(subpath, code_only, yaml_loader):
    """Check structure can be parsed from jinja templated files."""
    assert_structure(
        yaml_loader, "test/fixtures/templater/" + subpath, code_only=code_only
    )
