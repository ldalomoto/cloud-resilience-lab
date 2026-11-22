from dataclasses import dataclass
from src.circuit_breaker import CircuitBreaker, CircuitOpenError
from src.config import ResilienceConfig
from src.downstream_client import (
    DownstreamTimeoutError,
    DownstreamUnavailableError,
    call_downstream_service,
)
from src.retry_policy import execute_with_retry


@dataclass
class QueryOutcome:
    status: str
    attempts: int
    circuit_state: str
    instance_id: str
    detail: str


class ResilienceService:
    """Coordinates circuit breaker, retry policy, and timeout-bounded downstream calls."""

    def __init__(self, config: ResilienceConfig, breaker: CircuitBreaker) -> None:
        self.config = config
        self.breaker = breaker

    async def process_query(self, mode: str) -> QueryOutcome:
        try:
            self.breaker.allow_request()
        except CircuitOpenError as exc:
            return QueryOutcome(
                status="CIRCUIT_OPEN",
                attempts=0,
                circuit_state=self.breaker.state.value,
                instance_id=self.config.instance_id,
                detail=str(exc),
            )

        async def _attempt() -> str:
            return await call_downstream_service(
                mode=mode,
                timeout_sec=self.config.request_timeout_sec,
                slow_delay_sec=self.config.slow_mode_delay_sec,
            )

        try:
            message, attempts = await execute_with_retry(
                operation=_attempt,
                max_retries=self.config.max_retries,
                base_backoff_sec=self.config.base_backoff_sec,
                retryable_exceptions=(DownstreamTimeoutError, DownstreamUnavailableError),
            )
            self.breaker.record_success()
            status = "RETRY_OK" if attempts > 1 else "OK"
            return QueryOutcome(
                status=status,
                attempts=attempts,
                circuit_state=self.breaker.state.value,
                instance_id=self.config.instance_id,
                detail=message,
            )
        except DownstreamTimeoutError as exc:
            self.breaker.record_failure()
            return QueryOutcome(
                status="TIMEOUT_ERROR",
                attempts=self.config.max_retries + 1,
                circuit_state=self.breaker.state.value,
                instance_id=self.config.instance_id,
                detail=str(exc),
            )
        except DownstreamUnavailableError as exc:
            self.breaker.record_failure()
            return QueryOutcome(
                status="DOWNSTREAM_ERROR",
                attempts=self.config.max_retries + 1,
                circuit_state=self.breaker.state.value,
                instance_id=self.config.instance_id,
                detail=str(exc),
            )
