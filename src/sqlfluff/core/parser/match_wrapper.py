"""Defined the `match_wrapper` which adds validation and logging to match methods."""

from typing import Any, Callable, Tuple, TYPE_CHECKING

from sqlfluff.core.parser.match_logging import ParseMatchLogObject
from sqlfluff.core.parser.match_result import MatchResult
from sqlfluff.core.parser.helpers import join_segments_raw_curtailed

if TYPE_CHECKING:  # pragma: no cover
    from sqlfluff.core.parser.context import ParseContext
    from sqlfluff.core.parser import BaseSegment


MatchFuncType = Callable[[Any, Tuple["BaseSegment", ...], ParseContext], MatchResult]


class WrapParseMatchLogObject(ParseMatchLogObject):
    """A specialised version of ParseMatchLogObject.

    This defers some of the specialist handling to later.
    """

    def __init__(
        self, match: MatchResult, segments: Tuple["BaseSegment", ...], **kwargs: Any
    ) -> None:
        self.match = match
        self.segments = segments
        super().__init__(msg="OUT", match=match, **kwargs)

    def __str__(self) -> str:
        if self.match.is_complete():
            self.kwargs["symbol"] = "++"
        elif self.match:
            self.kwargs["symbol"] = "+"
        self.kwargs["seg"] = repr(join_segments_raw_curtailed(self.segments))
        return super().__str__()


def match_wrapper(v_level: int = 3) -> Callable[[MatchFuncType], MatchFuncType]:
    """Wraps a .match() method to add validation and logging.

    This is designed to be used as follows:

        class SomeMatchableObject(object):
            @match_wrapper()
            def match(self, segments, parse_context):
                ...
                return m

    This applies a common logging framework to both Grammar and
    Segment based match routines.
    """

    def inner_match_wrapper(func: MatchFuncType) -> MatchFuncType:
        """Decorate a match function."""

        def wrapped_match_method(
            self_cls: Any,
            segments: Tuple["BaseSegment", ...],
            parse_context: "ParseContext",
        ) -> MatchResult:
            """A wrapper on the match function to do some basic validation."""
            # Do the match
            m = func(self_cls, segments, parse_context)

            name = getattr(self_cls, "__name__", self_cls.__class__.__name__)

            # Validate result
            if not isinstance(m, MatchResult):  # pragma: no cover
                parse_context.logger.warning(
                    f"{name}.match, returned {type(m)} rather than MatchResult"
                )

            # Log the result.
            WrapParseMatchLogObject(
                grammar=name,
                func="match",
                match=m,
                parse_context=parse_context,
                segments=segments,
                v_level=v_level,
            ).log()

            # Basic Validation, skipped here because it still happens in the parse
            # commands.
            return m

        return wrapped_match_method

    return inner_match_wrapper
