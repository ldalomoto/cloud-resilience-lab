"""Unit tests for the Timeout pattern (downstream client)."""
import asyncio
import time
import unittest

from src.downstream_client import (
    DownstreamTimeoutError,
    DownstreamUnavailableError,
    call_downstream_service,
)


class TimeoutTests(unittest.TestCase):
    def test_normal_mode_finishes_within_timeout(self) -> None:
        result = asyncio.run(call_downstream_service("normal", timeout_sec=1.0, slow_delay_sec=2.0))
        self.assertIn("successfully", result)

    def test_slow_mode_exceeds_timeout(self) -> None:
        with self.assertRaises(DownstreamTimeoutError):
            asyncio.run(call_downstream_service("lento", timeout_sec=0.1, slow_delay_sec=0.5))

    def test_timeout_cuts_the_call_instead_of_waiting_for_it(self) -> None:
        start = time.monotonic()
        with self.assertRaises(DownstreamTimeoutError):
            asyncio.run(call_downstream_service("lento", timeout_sec=0.1, slow_delay_sec=2.0))
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 1.0, "call should be cut near 0.1s, not wait the full 2s")

    def test_down_mode_raises_unavailable(self) -> None:
        with self.assertRaises(DownstreamUnavailableError):
            asyncio.run(call_downstream_service("caido", timeout_sec=1.0, slow_delay_sec=2.0))


if __name__ == "__main__":
    unittest.main()
