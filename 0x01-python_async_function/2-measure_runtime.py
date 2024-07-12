#!/usr/bin/env python3
"""
Measure the runtime of wait_n function
"""
import asyncio
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


async def measure_time(n: int, max_delay: int) -> float:
    """
    Measures the total execution time for wait_n(n, max_delay),
    and returns the average time per call.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): Maximum delay for wait_random.

    Returns:
        float: Average time per call.
    """
    start_time = time.perf_counter() # perf_counter used for more precise timing
    await wait_n(n, max_delay)
    total_time = time.perf_counter() - start_time
    return total_time / n
