import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def execute_with_retry(
    operation: Callable[[], Awaitable[T]],
    max_retries: int,
    base_backoff_sec: float,
    retryable_exceptions: tuple[type[Exception], ...],
) -> tuple[T, int]:
    """Executes an async operation with exponential backoff on transient failures."""
    attempts = 0
    while True:
        attempts += 1
        try:
            result = await operation()
            return result, attempts
        except retryable_exceptions:
            if attempts > max_retries:
                raise
            backoff = base_backoff_sec * (2 ** (attempts - 1))
            await asyncio.sleep(backoff)
