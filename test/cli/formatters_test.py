"""The Test file for CLI Formatters."""

import re

from sqlfluff.core.rules.base import RuleGhost
from sqlfluff.core.parser import RawSegment
from sqlfluff.core.parser.markers import FilePositionMarker
from sqlfluff.core.errors import SQLLintError
from sqlfluff.cli.formatters import format_filename, format_violation


def escape_ansi(line):
    """Remove ANSI color codes for testing."""
    ansi_escape = re.compile(u"\u001b\\[[0-9]+(;[0-9]+)?m")
    return ansi_escape.sub("", line)


def test__cli__formatters__filename_nocol():
    """Test formatting filenames."""
    res = format_filename("blahblah", success=True)
    assert escape_ansi(res) == "== [blahblah] PASS"


def test__cli__formatters__violation():
    """Test formatting violations.

    NB Position is 1 + start_pos.
    """
    s = RawSegment("foobarbar", FilePositionMarker(0, 20, 11, 100))
    r = RuleGhost("A", "DESC")
    v = SQLLintError(segment=s, rule=r)
    f = format_violation(v)
    assert escape_ansi(f) == "L:  20 | P:  11 |    A | DESC"
