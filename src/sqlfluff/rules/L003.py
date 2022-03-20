"""Implementation of Rule L003."""
import dataclasses
import itertools
from typing import Dict, List, Optional, Sequence, Tuple

from sqlfluff.core.parser import WhitespaceSegment
from sqlfluff.core.parser.segments import BaseSegment
from sqlfluff.core.rules.functional import rsp, sp, Segments
from sqlfluff.core.rules.base import BaseRule, LintResult, LintFix, RuleContext
from sqlfluff.core.rules.doc_decorators import (
    document_fix_compatible,
    document_configuration,
)
from sqlfluff.core.templaters import TemplatedFile
from sqlfluff.core.templaters.base import RawFileSlice


@dataclasses.dataclass
class _LineSummary:
    """A dataobject to represent a line.

    Doubles as a memory object (holding state)
    that can be converted to a fresh summary instance
    """

    line_no: int = 0
    templated_line: Optional[int] = None
    line_buffer: List[BaseSegment] = dataclasses.field(default_factory=list)
    indent_buffer: List[BaseSegment] = dataclasses.field(default_factory=list)
    indent_size: int = 1

    # The final balance of a line once fully considered
    indent_balance: int = 0
    # The indent as it was once we say this lines "Anchor"
    anchor_indent_balance: int = 0
    hanging_indent: Optional[int] = None
    clean_indent: bool = True
    templated_line_type: Optional[str] = None
    is_comment_line: bool = False
    is_empty_line: bool = False
    line_anchor: Optional[BaseSegment] = None
    # These are only required for carrying state between lines
    line_indent_stack: List[int] = dataclasses.field(default_factory=list)
    hanger_pos: Optional[int] = None

    def __repr__(self) -> str:
        """Printable Summary without Segments."""
        keys_to_strip = (
            "line_buffer",
            "indent_buffer",
            "as_of_anchor",
        )
        print_dict: Dict = {
            key: value
            for key, value in self.__dict__.copy().items()
            if key not in keys_to_strip
        }

        return print_dict.__repr__()

    @property
    def template_content(self):  # pragma: no cover
        return "".join(
            seg.raw or getattr(seg, "source_str", "") for seg in self.line_buffer
        )

    def memory_line_reset(self):
        """When acting like a MemoryLine this resets state."""
        self.templated_line = False
        self.indent_buffer = []
        # N.B the clean indent depends on the buffer of the line just pased
        self.clean_indent = _is_clean_indent(self.line_buffer)
        self.line_buffer = []
        self.line_indent_stack = []
        self.indent_size = 0
        self.hanger_pos = None
        self.line_anchor = None
        self.templated_line_type = None
        return self

    def from_memo_line(self, line_no: int, templated_file: Optional[TemplatedFile]):
        """Create a final summary from a memo/marker line."""
        copied_line_buffer = self.line_buffer[:]
        # Generate our line summary based on the current state of the MemoLine
        is_comment_line = all(
            seg.is_type(
                "whitespace", "comment", "indent"  # dedent is a subtype of indent
            )
            for seg in copied_line_buffer
        )
        is_empty_line = not any(
            elem.is_code or elem.is_type("placeholder") for elem in copied_line_buffer
        )
        line_summary = self.__class__(
            line_no=line_no,
            templated_line=self.templated_line,
            # Using slicing to copy line_buffer here to be py2 compliant
            line_buffer=copied_line_buffer,
            indent_buffer=self.indent_buffer,
            indent_size=self.indent_size,
            indent_balance=self.indent_balance,
            anchor_indent_balance=self.anchor_indent_balance,
            hanging_indent=self.hanger_pos if self.line_indent_stack else None,
            # Clean indent is true if the line *ends* with an indent
            # or has an indent in the initial whitespace.
            clean_indent=self.clean_indent,
            # Solidify expensive immutable characteristics
            templated_line_type=_get_template_block_type(
                copied_line_buffer, templated_file
            ),
            is_comment_line=is_comment_line,
            is_empty_line=is_empty_line,
        )
        # Rest this object so it can continue to be used to track current state
        self.memory_line_reset()
        return line_summary

    def set_state_as_of_anchor(
        self,
        anchor: Optional[BaseSegment],
        tab_space_size: int,
    ):
        """Create a Line state of this line upon reaching the anchor."""
        self.anchor_indent_balance = self.indent_balance
        self.indent_size = _indent_size(
            self.indent_buffer,
            tab_space_size=tab_space_size,
        )
        self.line_anchor = anchor

        return self


def _copy_line_summary(line: _LineSummary) -> _LineSummary:
    new_line = _LineSummary(**line.__dict__.copy())
    list_keys = [
        "line_buffer",
        "indent_buffer",
        "line_indent_stack",
    ]
    for key in list_keys:
        el = new_line.__getattribute__(key)
        new_line.__setattr__(key, el[:])
    return new_line


def _is_clean_indent(prev_line_buffer: List[BaseSegment]):
    """Check the previous line to see if the current state is a clean indent."""
    # Assume an unclean indent, but if the last line
    # ended with an indent then we might be ok.
    # Was there an indent after the last code element of the previous line?
    for search_elem in reversed(prev_line_buffer):
        is_meta = search_elem.is_meta
        if not search_elem.is_code and not is_meta:
            continue
        if is_meta and search_elem.indent_val > 0:  # type: ignore
            return True
        break

    return False


@dataclasses.dataclass
class _Memory:
    # problem_lines keeps track of lines with problems so that we
    # don't compare to them.
    problem_lines: List[int] = dataclasses.field(default_factory=list)
    # hanging_lines keeps track of hanging lines so that we don't
    # compare to them when assessing indent.
    hanging_lines: List[int] = dataclasses.field(default_factory=list)
    # comment_lines keeps track of lines which are all comment.
    comment_lines: List[int] = dataclasses.field(default_factory=list)
    # Dict of processed lines
    line_summaries: Dict[int, _LineSummary] = dataclasses.field(default_factory=dict)

    in_indent: bool = True
    trigger: Optional[BaseSegment] = None


@document_fix_compatible
@document_configuration
class Rule_L003(BaseRule):
    """Indentation not consistent with previous lines.

    **Anti-pattern**

    The ``•`` character represents a space.
    In this example, the third line contains five spaces instead of four.

    .. code-block:: sql
       :force:

        SELECT
        ••••a,
        •••••b
        FROM foo


    **Best practice**

    Change the indentation to use a multiple of four spaces.

    .. code-block:: sql
       :force:

        SELECT
        ••••a,
        ••••b
        FROM foo

    """

    targets_templated = True
    _works_on_unparsable = False
    _adjust_anchors = True
    _ignore_types: List[str] = ["script_content"]
    config_keywords = ["tab_space_size", "indent_unit"]

    @staticmethod
    def _make_indent(
        num: int = 1, tab_space_size: int = 4, indent_unit: str = "space"
    ) -> str:
        if indent_unit == "tab":
            return "\t" * num
        if indent_unit == "space":
            return " " * tab_space_size * num

        raise ValueError(
            f"Parameter indent_unit has unexpected value: `{indent_unit}`. Expected"
            " `tab` or `space`."
        )

    @staticmethod
    def _segment_length(elem: BaseSegment, tab_space_size: int):
        return _segment_length(elem, tab_space_size)

    @staticmethod
    def _indent_size(segments: Sequence[BaseSegment], tab_space_size: int = 4) -> int:
        return _indent_size(segments, tab_space_size)

    @classmethod
    def _process_raw_stack(
        cls,
        raw_stack: Tuple[BaseSegment, ...],
        memory: _Memory,
        tab_space_size: int = 4,
        templated_file: Optional[TemplatedFile] = None,
    ) -> Dict[int, _LineSummary]:
        """Take the raw stack, split into lines and evaluate some stats."""
        result_buffer: Dict[int, _LineSummary] = memory.line_summaries
        memo_size = len(result_buffer)
        memo_line = (
            _copy_line_summary(result_buffer[memo_size])
            if memo_size
            else _LineSummary()
        )
        memo_line.memory_line_reset()
        line_no = 1
        started = line_no == (memo_size + 1)
        for elem in raw_stack:
            is_newline = elem.is_type("newline")
            # the below line act to reduce recalculation
            if not started:
                if is_newline:
                    line_no += 1
                started = line_no == (memo_size + 1)
                continue

            memo_line.line_buffer.append(elem)
            # Pin indent_balance to above zero
            if memo_line.indent_balance < 0:
                memo_line.indent_balance = 0

            if is_newline:
                result_buffer[line_no] = memo_line.from_memo_line(
                    line_no, templated_file
                )
                line_no += 1
                # Set the "templated_line" flag for the *next* line if the
                # newline that ended the *current* line was in templated space.
                # Reason: We want to ignore indentation of lines that are not
                # present in the raw (pre-templated) code.
                memo_line.templated_line = elem.is_templated
                continue

            if memo_line.line_anchor is None:
                memo_line = cls._process_pre_anchor(
                    elem, memo_line, tab_space_size
                )
                # If we hit the trigger element, stop processing.
                if elem is memory.trigger:
                    break
                continue

            if elem.is_meta and elem.indent_val != 0:  # type: ignore
                memo_line = cls._process_line_indents(elem, memo_line, tab_space_size)
                continue

            elif elem.is_code and memo_line.hanger_pos is None:
                memo_line.hanger_pos = cls._indent_size(
                    memo_line.line_buffer[:-1], tab_space_size=tab_space_size
                )

        # If we get to the end, and still have a buffer, add it on
        if memo_line.line_buffer:
            result_buffer[line_no] = memo_line.from_memo_line(
                line_no,
                templated_file,
            )
        return result_buffer

    @classmethod
    def _process_line_indents(
        cls,
        elem: BaseSegment,
        memo_line: _LineSummary,
        tab_space_size: int,
    ) -> _LineSummary:
        memo_line.indent_balance += elem.indent_val  # type: ignore
        if elem.indent_val > 0:  # type: ignore
            # Keep track of the indent at the last ... indent
            memo_line.line_indent_stack.append(
                cls._indent_size(memo_line.line_buffer, tab_space_size=tab_space_size)
            )
            memo_line.hanger_pos = None
            return memo_line
        # this is a dedent, we could still have a hanging indent,
        # but only if there's enough on the stack
        if memo_line.line_indent_stack:
            memo_line.line_indent_stack.pop()
        return memo_line

    @classmethod
    def _process_pre_anchor(
        cls,
        elem: BaseSegment,
        memo_line: _LineSummary,
        tab_space_size: int,
    ) -> _LineSummary:
        if elem.is_whitespace:
            memo_line.indent_buffer.append(elem)
            return memo_line
        if elem.is_meta and elem.indent_val != 0:  # type: ignore
            memo_line.indent_balance += elem.indent_val  # type: ignore
            if elem.indent_val > 0:  # type: ignore
                # a "clean" indent is one where it contains
                # an increase in indentation? Can't quite
                # remember the logic here. Let's go with that.
                memo_line.clean_indent = True
            return memo_line

        memo_line.set_state_as_of_anchor(elem, tab_space_size)
        return memo_line

    def _coerce_indent_to(
        self,
        desired_indent: str,
        current_indent_buffer: List[BaseSegment],
        current_anchor: BaseSegment,
    ) -> List[LintFix]:
        """Generate fixes to make an indent a certain size."""
        # In all cases we empty the existing buffer
        # except for our indent markers
        fixes = [
            LintFix.delete(elem)
            for elem in current_indent_buffer
            if not elem.is_type("indent")
        ]
        if len(desired_indent) == 0:
            # If there shouldn't be an indent at all, just delete.
            return fixes

        # Anything other than 0 create a fresh buffer
        return [
            LintFix.create_before(
                current_anchor,
                [
                    WhitespaceSegment(
                        raw=desired_indent,
                    ),
                ],
            ),
            *fixes,
        ]

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Indentation not consistent with previous lines.

        To set the default tab size, set the `tab_space_size` value
        in the appropriate configuration.

        We compare each line (first non-whitespace element of the
        line), with the indentation of previous lines. The presence
        (or lack) of indent or dedent meta-characters indicate whether
        the indent is appropriate.

        - Any line is assessed by the indent level at the first non
          whitespace element.
        - Any increase in indentation may be _up to_ the number of
          indent characters.
        - Any line must be in line with the previous line which had
          the same indent balance at its start.
        - Apart from "whole" indents, a "hanging" indent is possible
          if the line starts in line with either the indent of the
          previous line or if it starts at the same indent as the *last*
          indent meta segment in the previous line.

        """
        # Config type hints
        self.tab_space_size: int
        self.indent_unit: str
        segment = context.segment
        memory: _Memory = context.memory or _Memory()
        raw_stack: Tuple[BaseSegment, ...] = context.raw_stack
        if raw_stack and raw_stack[-1] is not context.segment:
            raw_stack = raw_stack + (segment,)

        is_ignorable = any(
            el.is_type(*self._ignore_types) for el in context.parent_stack + (segment,)
        )
        if is_ignorable:
            return LintResult(memory=memory)

        if segment.is_type("newline"):
            memory.in_indent = True
        elif memory.in_indent:
            is_non_raw_segment = bool(segment.segments)
            is_placeholder = segment.is_meta and segment.indent_val != 0  # type: ignore
            if not (segment.is_whitespace or is_non_raw_segment or is_placeholder):
                memory.in_indent = False
                # First non-whitespace element is our trigger
                memory.trigger = segment

        is_last = self.is_final_segment(context)
        if not segment.is_type("newline") and not is_last:
            # Process on line ends or file end
            return LintResult(memory=memory)

        line_summaries = self._process_raw_stack(
            raw_stack=raw_stack,
            memory=memory,
            tab_space_size=self.tab_space_size,
            templated_file=context.templated_file,
        )
        memory.line_summaries = line_summaries
        trigger_segment = memory.trigger
        memory.trigger = None
        if line_summaries and trigger_segment:
            last_line_no = max(line_summaries.keys())
            this_line = line_summaries[last_line_no]
            result = self._process_current_line(memory, trigger_segment)
            # Template lines don't need fixes
            # However we do need the mutations from the processing.
            if not this_line.templated_line:
                return result

        return LintResult(memory=memory)

    def _process_current_line(
        self,
        memory: _Memory,
        trigger_segment: BaseSegment,
    ) -> LintResult:
        """Checks indentation of one line of code, returning a LintResult.

        The _eval() function calls it for the current line of code:
        - When passed a newline segment (thus ending a line)
        - When passed the *final* segment in the entire parse tree (which may
          not be a newline)
        """
        res = memory.line_summaries
        this_line_no = max(res.keys())
        this_line: _LineSummary = res.pop(this_line_no)
        self.logger.debug(
            "Evaluating line #%s. %s",
            this_line_no,
            # Don't log the line or indent buffer, it's too noisy.
            this_line,
        )

        if this_line.is_comment_line:
            # Comment line, deal with it later.
            memory.comment_lines.append(this_line_no)
            self.logger.debug("    Comment Line. #%s", this_line_no)
            return LintResult(memory=memory)

        last_line = _find_last_meaningful_line(res)
        if len(res) > 0 and last_line:
            # Let's just deal with hanging indents here.
            if (
                # NB: Hangers are only allowed if there was content after the last
                # indent on the previous line. Otherwise it's just an indent.
                this_line.indent_size == last_line.hanging_indent
                # Or they're if the indent balance is the same and the indent is the
                # same AND the previous line was a hanger
                or (
                    this_line.indent_size == last_line.indent_size
                    and this_line.anchor_indent_balance
                    == last_line.anchor_indent_balance
                    and last_line.line_no in memory.hanging_lines
                )
            ) and (
                # There MUST also be a non-zero indent. Otherwise we're just on the
                # baseline.
                this_line.indent_size
                > 0
            ):
                # This is a HANGER
                memory.hanging_lines.append(this_line_no)
                self.logger.debug("    Hanger Line. #%s", this_line_no)
                self.logger.debug("    Last Line: %s", last_line)
                return LintResult(memory=memory)

        # Is this an indented first line?
        elif len(res) == 0:
            if this_line.indent_size > 0:
                self.logger.debug("    Indented First Line. #%s", this_line_no)
                return LintResult(
                    anchor=trigger_segment,
                    memory=memory,
                    description="First line has unexpected indent",
                    fixes=[LintFix.delete(elem) for elem in this_line.indent_buffer],
                )

        previous_line_numbers = sorted(res.keys(), reverse=True)
        # Special handling for template end blocks on a line by themselves.
        if this_line.templated_line_type == "end":
            # For a template block end on a line by itself, search for a
            # matching block start on a line by itself. If there is one, match
            # its indentation. Question: Could we avoid treating this as a
            # special case? It has some similarities to the non-templated test
            # case test/fixtures/linter/indentation_error_contained.sql, in tha
            # both have lines where anchor_indent_balance drops 2 levels from one line
            # to the next, making it a bit unclear how to indent that line.
            template_block_level = -1
            for k in previous_line_numbers:
                template_line: _LineSummary = res[k]
                if not template_line.templated_line_type:
                    continue
                if template_line.templated_line_type == "end":
                    template_block_level -= 1
                else:
                    template_block_level += 1

                if template_block_level != 0:
                    continue

                # Found prior template block line with the same indent balance.

                # Is this a problem line?
                if k in memory.problem_lines + memory.hanging_lines:
                    # Skip it if it is
                    return LintResult(memory=memory)

                self.logger.debug("    [template block end] Comparing to #%s", k)
                if this_line.indent_size == template_line.indent_size:
                    # All good.
                    return LintResult(memory=memory)

                # Indents don't match even though balance is the same...
                memory.problem_lines.append(this_line_no)

                # The previous indent.
                desired_indent = "".join(
                    elem.raw for elem in template_line.indent_buffer
                )

                # Make fixes
                first_non_indent_i = len(this_line.indent_buffer)
                current_anchor = this_line.line_buffer[first_non_indent_i]
                fixes = self._coerce_indent_to(
                    desired_indent=desired_indent,
                    current_indent_buffer=this_line.indent_buffer,
                    current_anchor=current_anchor,
                )
                self.logger.debug(
                    "    !! Indentation does not match #%s. Fixes: %s", k, fixes
                )
                return LintResult(
                    anchor=trigger_segment,
                    memory=memory,
                    description="Indentation not consistent with line #{}".format(k),
                    # See above for logic
                    fixes=fixes,
                )

        # Assuming it's not a hanger, let's compare it to the other previous
        # lines. We do it in reverse so that closer lines are more relevant.
        for k in previous_line_numbers:
            prev_line: _LineSummary = res[k]
            # Is this a problem line?
            if k in memory.problem_lines + memory.hanging_lines:
                # Skip it if it is
                continue

            # Is this an empty line?
            if prev_line.is_empty_line:
                # Skip if it is
                continue

            # Work out the difference in indent
            indent_diff = (
                this_line.anchor_indent_balance - prev_line.anchor_indent_balance
            )
            # If we're comparing to a previous, more deeply indented line, then skip and
            # keep looking.
            if indent_diff < 0:
                continue

            # Is the indent balance the same?
            if indent_diff == 0:
                self.logger.debug("    [same indent balance] Comparing to #%s", k)
                if this_line.indent_size != prev_line.indent_size:
                    # Indents don't match even though balance is the same...
                    memory.problem_lines.append(this_line_no)

                    # Work out desired indent
                    if prev_line.indent_size == 0:
                        desired_indent = ""
                    elif this_line.indent_size == 0:
                        desired_indent = self._make_indent(
                            indent_unit=self.indent_unit,
                            tab_space_size=self.tab_space_size,
                        )
                    else:
                        # The previous indent.
                        desired_indent = "".join(
                            elem.raw for elem in prev_line.indent_buffer
                        )

                    # Make fixes
                    fixes = self._coerce_indent_to(
                        desired_indent=desired_indent,
                        current_indent_buffer=this_line.indent_buffer,
                        current_anchor=trigger_segment,
                    )
                    self.logger.debug(
                        "    !! Indentation does not match #%s. Fixes: %s", k, fixes
                    )
                    return LintResult(
                        anchor=trigger_segment,
                        memory=memory,
                        description="Indentation not consistent with line #{}".format(
                            k
                        ),
                        # See above for logic
                        fixes=fixes,
                    )
            # Are we at a deeper indent?
            elif indent_diff > 0:
                self.logger.debug("    [deeper indent balance] Comparing to #%s", k)
                # NB: We shouldn't need to deal with correct hanging indents
                # here, they should already have been dealt with before. We
                # may still need to deal with *creating* hanging indents if
                # appropriate.
                self.logger.debug("    Comparison Line: %s", prev_line)

                # Check to see if we've got a whole number of multiples. If
                # we do then record the number for later, otherwise raise
                # an error. We do the comparison here so we have a reference
                # point to do the repairs. We need a sensible previous line
                # to base the repairs off. If there's no indent at all, then
                # we should also take this route because there SHOULD be one.
                if this_line.indent_size % self.tab_space_size != 0:
                    memory.problem_lines.append(this_line_no)

                    # The default indent is the one just reconstructs it from
                    # the indent size.
                    default_indent = "".join(
                        elem.raw for elem in prev_line.indent_buffer
                    ) + self._make_indent(
                        indent_unit=self.indent_unit,
                        tab_space_size=self.tab_space_size,
                        num=indent_diff,
                    )
                    # If we have a clean indent, we can just add steps in line
                    # with the difference in the indent buffers. simples.
                    if this_line.clean_indent:
                        self.logger.debug("        Use clean indent.")
                        desired_indent = default_indent
                    # If we have the option of a hanging indent then use it.
                    elif prev_line.hanging_indent:
                        self.logger.debug("        Use hanging indent.")
                        desired_indent = " " * prev_line.hanging_indent
                    else:  # pragma: no cover
                        self.logger.debug("        Use default indent.")
                        desired_indent = default_indent

                    fixes = self._coerce_indent_to(
                        desired_indent=desired_indent,
                        current_indent_buffer=this_line.indent_buffer,
                        current_anchor=trigger_segment,
                    )
                    return LintResult(
                        anchor=trigger_segment,
                        memory=memory,
                        description=(
                            "Indentation not hanging or a multiple of {} spaces"
                        ).format(self.tab_space_size),
                        fixes=fixes,
                    )

                this_indent_num = this_line.indent_size // self.tab_space_size
                # We know that the indent balance is higher, what actually is
                # the difference in indent counts? It should be a whole number
                # if we're still here.
                comp_indent_num = prev_line.indent_size // self.tab_space_size

                # The indent number should be at least 1, and can be UP TO
                # and including the difference in the indent balance.
                if comp_indent_num == this_indent_num:
                    # We have two lines indented the same, but with a different starting
                    # indent balance. This is either a problem OR a sign that one of the
                    # opening indents wasn't used. We account for the latter and then
                    # have a violation if that wasn't the case.

                    # Does the comparison line have enough unused indent to get us back
                    # to where we need to be? NB: This should only be applied if this is
                    # a CLOSING bracket.

                    # First work out if we have some closing brackets, and if so, how
                    # many.
                    b_idx = 0
                    b_num = 0
                    while True:
                        if len(this_line.line_buffer[b_idx:]) == 0:
                            break

                        elem = this_line.line_buffer[b_idx]
                        if not elem.is_code:
                            b_idx += 1
                            continue
                        else:
                            if elem.is_type("end_bracket", "end_square_bracket"):
                                b_idx += 1
                                b_num += 1
                                continue
                            break  # pragma: no cover

                    if b_num < indent_diff:
                        # It doesn't. That means we *should* have an indent when
                        # compared to this line and we DON'T.
                        memory.problem_lines.append(this_line_no)
                        return LintResult(
                            anchor=trigger_segment,
                            memory=memory,
                            description="Indent expected and not found compared to line"
                            " #{}".format(k),
                            # Add in an extra bit of whitespace for the indent
                            fixes=[
                                LintFix.create_before(
                                    trigger_segment,
                                    [
                                        WhitespaceSegment(
                                            raw=self._make_indent(
                                                indent_unit=self.indent_unit,
                                                tab_space_size=self.tab_space_size,
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        )
                elif this_indent_num < comp_indent_num:
                    memory.problem_lines.append(this_line_no)
                    return LintResult(
                        anchor=trigger_segment,
                        memory=memory,
                        description="Line under-indented compared to line #{}".format(
                            k
                        ),
                        fixes=[
                            LintFix.create_before(
                                trigger_segment,
                                [
                                    WhitespaceSegment(
                                        # Make the minimum indent for it to be ok.
                                        raw=self._make_indent(
                                            num=comp_indent_num - this_indent_num,
                                            indent_unit=self.indent_unit,
                                            tab_space_size=self.tab_space_size,
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    )
                elif this_indent_num > comp_indent_num + indent_diff:
                    memory.problem_lines.append(this_line_no)
                    # Calculate the lowest ok indent:
                    desired_indent = self._make_indent(
                        num=comp_indent_num - this_indent_num,
                        indent_unit=self.indent_unit,
                        tab_space_size=self.tab_space_size,
                    )

                    fixes = self._coerce_indent_to(
                        desired_indent=desired_indent,
                        current_indent_buffer=this_line.indent_buffer,
                        current_anchor=trigger_segment,
                    )

                    return LintResult(
                        anchor=trigger_segment,
                        memory=memory,
                        description="Line over-indented compared to line #{}".format(k),
                        fixes=fixes,
                    )

            # This was a valid comparison, so if it doesn't flag then
            # we can assume that we're ok.
            self.logger.debug("    Indent deemed ok comparing to #%s", k)
            comment_fix = self._calculate_comment_fixes(
                memory, previous_line_numbers, this_line
            )
            return comment_fix or LintResult(memory=memory)

            # NB: At shallower indents, we don't check, we just check the
            # previous lines with the same balance. Deeper indents can check
            # themselves.

        # If we get to here, then we're all good for now.
        return LintResult(memory=memory)

    def _calculate_comment_fixes(
        self, memory: _Memory, previous_line_numbers: List[int], this_line: _LineSummary
    ) -> Optional[LintResult]:
        # Given that this line is ok, consider if the preceding lines are
        # comments. If they are, lint the indentation of the comment(s).
        fixes: List[LintFix] = []
        anchor: Optional[BaseSegment] = None
        for n in previous_line_numbers:
            if n not in memory.comment_lines:
                break
            # The previous line WAS a comment.
            prev_line = memory.line_summaries[n]
            if this_line.indent_size != prev_line.indent_size:
                # It's not aligned.
                # Find the anchor first.
                for seg in prev_line.line_buffer:
                    if seg.is_type("comment"):
                        anchor = seg
                        break

                if not anchor:  # pragma: no cover
                    continue
                # Make fixes.
                fixes += self._coerce_indent_to(
                    desired_indent="".join(
                        elem.raw for elem in this_line.indent_buffer
                    ),
                    current_indent_buffer=prev_line.indent_buffer,
                    current_anchor=anchor,
                )

                memory.problem_lines.append(n)

        if not fixes:
            return None

        return LintResult(
            anchor=anchor,
            memory=memory,
            description="Comment not aligned with following line.",
            fixes=fixes,
        )


class _TemplateLineInterpreter:
    start_blocks = (
        ("placeholder", "block_start"),
        ("placeholder", "compound"),
        ("placeholder", "literal"),
        ("placeholder", "block_mid"),
    )
    indent_types = (
        ("indent", None),
        ("newline", None),
    )
    valid_start_combos = list(
        itertools.product(
            start_blocks,
            indent_types,
        )
    )
    dedent_types = (("dedent", None),)
    end_block = (
        ("placeholder", "block_end"),
        ("placeholder", "compound"),
        ("placeholder", "block_mid"),
    )
    valid_end_combos = list(
        itertools.product(
            dedent_types,
            end_block,
        )
    )

    def __init__(
        self,
        current_line: List[BaseSegment],
        templated_file: Optional[TemplatedFile],
    ) -> None:
        self.current_line = [el for el in current_line if not el.is_whitespace]
        self.templated_file = templated_file
        self._adjacent_pairs: Optional[
            List[Tuple[Tuple[str, Optional[str]], Tuple[str, Optional[str]]]]
        ] = None

    def is_single_placeholder_line(self):
        count_placeholder = 0
        for seg in self.current_line:
            if seg.is_code:
                return False
            elif seg.is_type("placeholder"):
                count_placeholder += 1
        return count_placeholder == 1

    def list_segement_and_raw_segement_types(self):
        """Yields the tuple of seg type and underlying type were applicable."""
        for seg in self.current_line:
            raw_seg = self.get_raw_slices(seg)
            yield (seg.type, raw_seg[0].slice_type if raw_seg else None)

    def get_adjacent_type_pairs(self):
        """Produce a list of pairs of each sequenctial combo of two."""
        if self._adjacent_pairs:
            return self._adjacent_pairs
        iterable = self.list_segement_and_raw_segement_types()
        a, b = itertools.tee(iterable)
        # consume the first item in b
        next(b, None)
        self._adjacent_pairs = list(zip(a, b))
        return self._adjacent_pairs

    def is_block_start(self):
        return any(
            pair in self.valid_start_combos for pair in self.get_adjacent_type_pairs()
        )

    def is_block_end(self):
        return any(
            pair in self.valid_end_combos for pair in self.get_adjacent_type_pairs()
        )

    def block_type(self) -> Optional[str]:
        """Return a block_type enum."""
        if not self.templated_file:
            return None

        if not self.is_single_placeholder_line():
            return None

        if self.is_block_end():
            return "end"

        if self.is_block_start():
            return "start"

        return None

    def get_raw_slices(self, elem: BaseSegment) -> Optional[List[RawFileSlice]]:
        if not self.templated_file:  # pragma: no cover
            return None

        if not elem.is_type("placeholder"):
            return None

        assert elem.pos_marker, "TypeGuard"
        slices = self.templated_file.raw_slices_spanning_source_slice(
            elem.pos_marker.source_slice
        )
        return slices or None


def _get_template_block_type(
    line_buffer: List[BaseSegment],
    templated_file: Optional[TemplatedFile] = None,
):
    """Convience fn for getting 'start', 'end' etc of a placeholder line."""
    template_info = _TemplateLineInterpreter(line_buffer, templated_file)
    return template_info.block_type()


def _segment_length(elem: BaseSegment, tab_space_size: int):
    # Start by assuming the typical case, where we need not consider slices
    # or templating.
    raw = elem.raw

    # If it's whitespace, it might be a mixture of literal and templated
    # whitespace. Check for this.
    if elem.is_type("whitespace") and elem.is_templated:
        # Templated case: Find the leading *literal* whitespace.
        assert elem.pos_marker
        templated_file = elem.pos_marker.templated_file
        # Extract the leading literal whitespace, slice by slice.
        raw = ""
        for raw_slice in Segments(
            elem, templated_file=templated_file
        ).raw_slices.select(loop_while=rsp.is_slice_type("literal")):
            # Compute and append raw_slice's contribution.
            raw += sp.raw_slice(elem, raw_slice)

    # convert to spaces for convenience (and hanging indents)
    return raw.replace("\t", " " * tab_space_size)


def _indent_size(segments: Sequence[BaseSegment], tab_space_size: int = 4) -> int:
    indent_size = 0
    for elem in segments:
        raw = Rule_L003._segment_length(elem, tab_space_size)
        indent_size += len(raw)
    return indent_size


def _find_last_meaningful_line(
    line_summaries: Dict[int, _LineSummary]
) -> Optional[_LineSummary]:
    # Find last meaningful line indent.
    for k in sorted(line_summaries.keys(), reverse=True):
        line: _LineSummary = line_summaries[k]
        if any(seg.is_code for seg in line.line_buffer):
            return line

    return None
