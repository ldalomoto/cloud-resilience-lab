"""Integration tests: timeout + retry + circuit breaker working together."""
import asyncio
import unittest

from src.circuit_breaker import CircuitBreaker
from src.config import ResilienceConfig
from src.resilience_service import ResilienceService

# Small values so the tests run fast; the logic is identical to the real config.
FAST_CONFIG = ResilienceConfig(
    instance_id="test-instance",
    request_timeout_sec=0.2,  # must be above the 0.05s a "normal" call takes
    slow_mode_delay_sec=0.5,
    max_retries=2,
    base_backoff_sec=0.01,
    failure_threshold=3,
    recovery_timeout_sec=0.3,
)


def new_service() -> ResilienceService:
    breaker = CircuitBreaker(FAST_CONFIG.failure_threshold, FAST_CONFIG.recovery_timeout_sec)
    return ResilienceService(FAST_CONFIG, breaker)


def query(service: ResilienceService, mode: str):
    return asyncio.run(service.process_query(mode))


class ResilienceServiceTests(unittest.TestCase):
    def test_normal_mode_returns_ok_with_one_attempt(self) -> None:
        outcome = query(new_service(), "normal")
        self.assertEqual((outcome.status, outcome.attempts, outcome.circuit_state), ("OK", 1, "CLOSED"))

    def test_slow_mode_ends_in_timeout_error_after_all_attempts(self) -> None:
        outcome = query(new_service(), "lento")
        self.assertEqual(outcome.status, "TIMEOUT_ERROR")
        self.assertEqual(outcome.attempts, FAST_CONFIG.max_retries + 1)

    def test_down_mode_ends_in_downstream_error_after_all_attempts(self) -> None:
        outcome = query(new_service(), "caido")
        self.assertEqual(outcome.status, "DOWNSTREAM_ERROR")
        self.assertEqual(outcome.attempts, FAST_CONFIG.max_retries + 1)
        self.assertEqual(outcome.circuit_state, "CLOSED")

    def test_circuit_opens_after_three_failed_requests_and_then_rejects(self) -> None:
        service = new_service()
        states = [query(service, "caido").circuit_state for _ in range(3)]
        self.assertEqual(states, ["CLOSED", "CLOSED", "OPEN"])

        rejected = query(service, "caido")
        self.assertEqual(rejected.status, "CIRCUIT_OPEN")
        self.assertEqual(rejected.attempts, 0)

    def test_open_circuit_rejects_even_healthy_requests(self) -> None:
        service = new_service()
        for _ in range(3):
            query(service, "caido")
        self.assertEqual(query(service, "normal").status, "CIRCUIT_OPEN")

    def test_circuit_recovers_after_timeout_when_service_is_healthy(self) -> None:
        service = new_service()
        for _ in range(3):
            query(service, "caido")
        asyncio.run(asyncio.sleep(FAST_CONFIG.recovery_timeout_sec + 0.05))

        outcome = query(service, "normal")
        self.assertEqual((outcome.status, outcome.circuit_state), ("OK", "CLOSED"))

    def test_circuit_reopens_if_trial_request_fails(self) -> None:
        service = new_service()
        for _ in range(3):
            query(service, "caido")
        asyncio.run(asyncio.sleep(FAST_CONFIG.recovery_timeout_sec + 0.05))

        outcome = query(service, "caido")  # HALF_OPEN trial that fails
        self.assertEqual((outcome.status, outcome.circuit_state), ("DOWNSTREAM_ERROR", "OPEN"))


if __name__ == "__main__":
    unittest.main()
