#!/usr/bin/env python3
"""
Contains method that safely gets value from dictionar
"""
from typing import Mapping, Any, TypeVar, Union

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: T = None) -> Union[Any, T]:
    """
    Safely retrieves a value from a dictionary-like object
    """
    if key in dct:
        return dct[key]
    else:
        return default
