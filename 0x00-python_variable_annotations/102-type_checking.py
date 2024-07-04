#!/usr/bin/env python3
"""
This script defines a function zoom_array that zooms
in on a tuple by repeating each element based on given factor.
"""
from typing import Tuple, List, Any


def zoom_array(lst: Tuple[Any, ...], factor: int = 2) -> List[Any]:
    """
    Zooms into a tuple by repeating each element based on a given factor
    """
    zoomed_in: List[Any] = [
            item for item in lst
            for i in range(factor)
            ]
    return zoomed_in
