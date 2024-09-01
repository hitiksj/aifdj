"""Dict helpers, mostly used in config routines."""

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union


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


def records_to_nested_dict(
    records: Iterable[Tuple[Tuple[str, ...], T]],
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


def nested_dict_get(
    dict_obj: NestedStringDict[T], keys: Sequence[str], key_index: int = 0
) -> Union[T, NestedStringDict[T]]:
    """Perform a lookup in a nested dict object.

    Lookups are performed by iterating keys.
    >>> nested_dict_get(
    ...     {"a": {"b": "c"}}, ("a", "b")
    ... )
    'c'

    Lookups may return sections of nested dicts.
    >>> nested_dict_get(
    ...     {"a": {"b": "c"}}, ("a",)
    ... )
    {'b': 'c'}

    Raises `KeyError` if any keys are not found.
    >>> nested_dict_get(
    ...     {"a": {"b": "c"}}, ("p", "q")
    ... )
    Traceback (most recent call last):
        ...
    KeyError: "'p' not found in nested dict lookup"

    Raises `KeyError` we run out of dicts before keys are exhausted.
    >>> nested_dict_get(
    ...     {"a": {"b": "d"}}, ("a", "b", "c")
    ... )
    Traceback (most recent call last):
        ...
    KeyError: "'b' found non dict value, but there are more keys to iterate: ('c',)"

    """
    assert keys, "Nested dict lookup called without keys."
    assert key_index < len(keys), "Key exhaustion on nested dict lookup"

    next_key = keys[key_index]
    if next_key not in dict_obj:
        raise KeyError(f"{next_key!r} not found in nested dict lookup")
    next_value = dict_obj[next_key]

    # Are we all the way through the keys?
    if key_index + 1 == len(keys):
        # NOTE: Could be a section or a value.
        return next_value

    # If we're not all the way through the keys, go deeper if we can.
    if not isinstance(next_value, dict):
        raise KeyError(
            f"{next_key!r} found non dict value, but there are more keys to "
            f"iterate: {keys[key_index + 1:]}"
        )

    return nested_dict_get(next_value, keys, key_index=key_index + 1)


def nested_dict_set(
    dict_obj: NestedStringDict[T],
    keys: Sequence[str],
    value: Union[T, NestedStringDict[T]],
    key_index: int = 0,
) -> None:
    """Set a value in a nested dict object.

    Lookups are performed by iterating keys.
    >>> d = {"a": {"b": "c"}}
    >>> nested_dict_set(d, ("a", "b"), "d")
    >>> d
    {'a': {'b': 'd'}}

    Values may set dicts.
    >>> d = {"a": {"b": "c"}}
    >>> nested_dict_set(d, ("a", "b"), {"d": "e"})
    >>> d
    {'a': {'b': {'d': 'e'}}}

    Any keys not found will be created.
    >>> d = {"a": {"b": "c"}}
    >>> nested_dict_set(d, ("p", "q"), "r")
    >>> d
    {'a': {'b': 'c'}, 'p': {'q': 'r'}}

    Values may be overwritten with sub keys.
    >>> d = {"a": {"b": "c"}}
    >>> nested_dict_set(d, ("a", "b", "d"), "e")
    >>> d
    {'a': {'b': {'d': 'e'}}}
    """
    assert keys, "Nested dict lookup called without keys."
    assert key_index < len(keys), "Key exhaustion on nested dict lookup"

    next_key = keys[key_index]
    # Create an empty dictionary if key not found.
    if next_key not in dict_obj:
        dict_obj[next_key] = {}
    # Overwrite the value to a dict if the existing value isn't one.
    elif not isinstance(dict_obj[next_key], dict):
        dict_obj[next_key] = {}
    next_value = dict_obj[next_key]
    assert isinstance(next_value, dict)

    # Do we have more keys to set?
    # If we do, recurse:
    if key_index + 1 < len(keys):
        nested_dict_set(next_value, keys=keys, value=value, key_index=key_index + 1)
    # If we don't, then just set the value:
    else:
        dict_obj[next_key] = value
