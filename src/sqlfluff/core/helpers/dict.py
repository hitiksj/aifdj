"""Dict helpers, mostly used in config routines."""

from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)


def nested_combine(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Combine an iterable of dictionaries.

    Each dictionary is combined into a result dictionary. For
    each key in the first dictionary, it will be overwritten
    by any same-named key in any later dictionaries in the
    iterable. If the element at that key is a dictionary, rather
    than just overwriting we use the same function to combine
    those dictionaries.

    Args:
        *dicts: An iterable of dictionaries to be combined.

    Returns:
        `dict`: A combined dictionary from the input dictionaries.

    A simple example:
    >>> nested_combine({"a": {"b": "c"}}, {"a": {"d": "e"}})
    {'a': {'b': 'c', 'd': 'e'}}

    Keys overwrite left to right:
    >>> nested_combine({"a": {"b": "c"}}, {"a": {"b": "e"}})
    {'a': {'b': 'e'}}
    """
    r: Dict[str, Any] = {}
    for d in dicts:
        for k in d:
            if k in r and isinstance(r[k], dict):
                if isinstance(d[k], dict):
                    r[k] = nested_combine(r[k], d[k])
                else:  # pragma: no cover
                    raise ValueError(
                        "Key {!r} is a dict in one config but not another! PANIC: "
                        "{!r}".format(k, d[k])
                    )
            else:
                r[k] = d[k]
    return r


def dict_diff(
    left: Dict[str, Any], right: Dict[str, Any], ignore: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Work out the difference between two dictionaries.

    Returns a dictionary which represents elements in the `left`
    dictionary which aren't in the `right` or are different to
    those in the `right`. If the element is a dictionary, we
    recursively look for differences in those dictionaries,
    likewise only returning the differing elements.

    NOTE: If an element is in the `right` but not in the `left`
    at all (i.e. an element has been *removed*) then it will
    not show up in the comparison.

    Args:
        left (:obj:`dict`): The object containing the *new* elements
            which will be compared against the other.
        right (:obj:`dict`): The object to compare against.
        ignore (:obj:`list` of `str`, optional): Keys to ignore.

    Returns:
        `dict`: A dictionary representing the difference.

    Basic functionality shown, especially returning the left as:
    >>> dict_diff({"a": "b", "c": "d"}, {"a": "b", "c": "e"})
    {'c': 'd'}

    Ignoring works on a key basis:
    >>> dict_diff({"a": "b"}, {"a": "c"})
    {'a': 'b'}
    >>> dict_diff({"a": "b"}, {"a": "c"}, ["a"])
    {}
    """
    buff: Dict[str, Any] = {}
    for k in left:
        if ignore and k in ignore:
            continue
        # Is the key there at all?
        if k not in right:
            buff[k] = left[k]
        # Is the content the same?
        elif left[k] == right[k]:
            continue
        # If it's not the same but both are dicts, then compare
        elif isinstance(left[k], dict) and isinstance(right[k], dict):
            diff = dict_diff(left[k], right[k], ignore=ignore)
            # Only include the difference if non-null.
            if diff:
                buff[k] = diff
        # It's just different
        else:
            buff[k] = left[k]
    return buff


T = TypeVar("T")

NestedStringDict = Dict[str, Union[T, "NestedStringDict[T]"]]
"""Nested dict, with keys as strings.

All values of the dict are either values of the given type variable T, or
are themselves dicts with the same nested properties. Variables of this type
are used regularly in configuration methods and classes.
"""

NestedDictRecord = Tuple[Tuple[str, ...], T]
"""Tuple form record of a setting in a NestedStringDict.

The tuple of strings in the first element is the "address" in the NestedStringDict
with the value as the second element on the tuple.
"""


def records_to_nested_dict(
    records: Iterable[NestedDictRecord[T]],
) -> NestedStringDict[T]:
    """Reconstruct records into a dict.

    >>> records_to_nested_dict(
    ...     [(("foo", "bar", "baz"), "a"), (("foo", "bar", "biz"), "b")]
    ... )
    {'foo': {'bar': {'baz': 'a', 'biz': 'b'}}}
    """
    result: NestedStringDict = {}
    for key, val in records:
        ref: NestedStringDict = result
        for step in key[:-1]:
            # If the subsection isn't there, make it.
            if step not in ref:
                ref[step] = {}
            # Then step into it.
            subsection = ref[step]
            assert isinstance(subsection, dict)
            ref = subsection
        ref[key[-1]] = val
    return result


def iter_records_from_nested_dict(
    nested_dict: NestedStringDict[T],
) -> Iterator[NestedDictRecord[T]]:
    """Walk a config dict and get config elements.

    >>> list(
    ...    iter_records_from_nested_dict(
    ...        {"foo":{"bar":{"baz": "a", "biz": "b"}}}
    ...    )
    ... )
    [(('foo', 'bar', 'baz'), 'a'), (('foo', 'bar', 'biz'), 'b')]
    """
    for key, val in nested_dict.items():
        if isinstance(val, dict):
            for partial_key, sub_val in iter_records_from_nested_dict(val):
                yield (key,) + partial_key, sub_val
        else:
            yield (key,), val
