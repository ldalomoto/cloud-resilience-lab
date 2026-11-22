"""Unit tests for the Circuit Breaker (state machine only, time is simulated)."""
import unittest
from unittest import mock

from src.circuit_breaker import CircuitBreaker, CircuitOpenError, CircuitState

THRESHOLD = 3
RECOVERY_SEC = 10.0


class FakeClock:
    """Replaces time.monotonic so tests do not need to wait for real seconds."""

    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class CircuitBreakerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = FakeClock()
        patcher = mock.patch("src.circuit_breaker.time.monotonic", self.clock)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.breaker = CircuitBreaker(THRESHOLD, RECOVERY_SEC)

    def open_circuit(self) -> None:
        for _ in range(THRESHOLD):
            self.breaker.record_failure()

    def test_starts_closed_and_allows_requests(self) -> None:
        self.assertEqual(self.breaker.state, CircuitState.CLOSED)
        self.breaker.allow_request()  # must not raise

    def test_stays_closed_below_threshold(self) -> None:
        for _ in range(THRESHOLD - 1):
            self.breaker.record_failure()
        self.assertEqual(self.breaker.state, CircuitState.CLOSED)

    def test_opens_when_threshold_is_reached(self) -> None:
        self.open_circuit()
        self.assertEqual(self.breaker.state, CircuitState.OPEN)

    def test_open_circuit_rejects_requests_immediately(self) -> None:
        self.open_circuit()
        with self.assertRaises(CircuitOpenError):
            self.breaker.allow_request()

    def test_success_resets_failure_counter(self) -> None:
        self.breaker.record_failure()
        self.breaker.record_failure()
        self.breaker.record_success()
        self.breaker.record_failure()
        self.breaker.record_failure()
        self.assertEqual(self.breaker.state, CircuitState.CLOSED)

    def test_stays_open_before_recovery_timeout(self) -> None:
        self.open_circuit()
        self.clock.advance(RECOVERY_SEC - 0.1)
        with self.assertRaises(CircuitOpenError):
            self.breaker.allow_request()
        self.assertEqual(self.breaker.state, CircuitState.OPEN)

    def test_becomes_half_open_after_recovery_timeout(self) -> None:
        self.open_circuit()
        self.clock.advance(RECOVERY_SEC)
        self.breaker.allow_request()  # lets the trial request through
        self.assertEqual(self.breaker.state, CircuitState.HALF_OPEN)

    def test_half_open_success_closes_circuit(self) -> None:
        self.open_circuit()
        self.clock.advance(RECOVERY_SEC)
        self.breaker.allow_request()
        self.breaker.record_success()
        self.assertEqual(self.breaker.state, CircuitState.CLOSED)

    def test_half_open_failure_reopens_circuit(self) -> None:
        self.open_circuit()
        self.clock.advance(RECOVERY_SEC)
        self.breaker.allow_request()
        self.breaker.record_failure()
        self.assertEqual(self.breaker.state, CircuitState.OPEN)
        with self.assertRaises(CircuitOpenError):
            self.breaker.allow_request()


if __name__ == "__main__":
    unittest.main()
