import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ResilienceConfig:
    instance_id: str = os.getenv("INSTANCE_ID", "backend-1")
    request_timeout_sec: float = float(os.getenv("REQUEST_TIMEOUT_SEC", "1.0"))
    slow_mode_delay_sec: float = float(os.getenv("SLOW_MODE_DELAY_SEC", "2.0"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "2"))
    base_backoff_sec: float = float(os.getenv("BASE_BACKOFF_SEC", "0.5"))
    failure_threshold: int = int(os.getenv("FAILURE_THRESHOLD", "3"))
    recovery_timeout_sec: float = float(os.getenv("RECOVERY_TIMEOUT_SEC", "10.0"))


CONFIG = ResilienceConfig()
