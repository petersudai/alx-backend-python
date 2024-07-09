#!/usr/bin/env python3
"""
1. Async Comprehensions
"""

import asyncio
from typing import List
from 0-async_generator import async_generator


async def async_comprehension() -> List[float]:
    """
    Coroutine that collects 10 random numbers using an async comprehension over async_generator.
    
    Returns:
        List[float]: A list of 10 random float numbers.
    """
    return [number async for number in async_generator()]
