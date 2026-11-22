import asyncio


class DownstreamTimeoutError(Exception):
    pass


class DownstreamUnavailableError(Exception):
    pass


async def call_downstream_service(mode: str, timeout_sec: float, slow_delay_sec: float) -> str:
    """Simulates a downstream call enforcing an explicit timeout boundary."""
    simulated_delay = slow_delay_sec if mode == "lento" else 0.05
    try:
        await asyncio.wait_for(asyncio.sleep(simulated_delay), timeout=timeout_sec)
    except asyncio.TimeoutError as exc:
        raise DownstreamTimeoutError(f"Downstream call exceeded {timeout_sec}s timeout") from exc

    if mode == "caido":
        raise DownstreamUnavailableError("Downstream service is currently unavailable")

    return "Downstream operation completed successfully"
