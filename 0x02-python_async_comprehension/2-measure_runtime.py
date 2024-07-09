#!/usr/bin/env python3
"""
2. Run time for four parallel comprehensions
"""

import asyncio
import time
from typing import List
from 1-async_comprehension import async_comprehension


async def measure_runtime() -> float:
    """
    Coroutine that measures the total runtime of executing async_comprehension four times in parallel.

    Returns:
        float: Total runtime in seconds.
    """
    start_time = time.perf_counter()
    
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )
    
    end_time = time.perf_counter()
    return end_time - start_time
