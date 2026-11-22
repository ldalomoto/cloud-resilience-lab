"""Live demo of Timeout + Retry + Circuit Breaker against a running backend.

Usage:  python scripts/demo_circuit_breaker.py [BASE_URL]
Default BASE_URL is http://localhost:8000 (the backend started by docker compose).
Uses only the Python standard library.
"""
import json
import sys
import time
import urllib.request
from datetime import datetime

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
RECOVERY_WAIT_SEC = 10.5  # backend RECOVERY_TIMEOUT_SEC is 10s


def query(step: int, label: str, mode: str) -> dict:
    body = json.dumps({"modo": mode, "payload": f"demo-{step}"}).encode()
    request = urllib.request.Request(
        f"{BASE_URL}/api/v1/consultar",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.monotonic()
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    elapsed_ms = (time.monotonic() - start) * 1000
    stamp = datetime.now().strftime("%H:%M:%S")
    print(
        f"[{stamp}] step {step:>2} | mode={mode:<6} | estado={data['estado']:<16} "
        f"| intentos={data['intentos']} | circuito={data['circuito']:<9} | {elapsed_ms:7.0f} ms"
    )
    print(f"           {label}")
    return data


def wait(seconds: float, reason: str) -> None:
    print(f"           ... waiting {seconds}s: {reason}")
    time.sleep(seconds)


def main() -> None:
    print(f"Target: {BASE_URL}\n")
    # Warm-up: the first connection can be slow and would distort the timings below.
    urllib.request.urlopen(f"{BASE_URL}/health", timeout=30).read()

    query(1, "Healthy service -> OK on the first attempt.", "normal")
    query(2, "Slow service -> every attempt hits the 1s TIMEOUT, retries x2, then TIMEOUT_ERROR.", "lento")
    query(3, "Healthy again -> success resets the breaker's failure counter.", "normal")

    print()
    query(4, "Service down -> 3 attempts fail (RETRY). Breaker failure 1/3, still CLOSED.", "caido")
    query(5, "Breaker failure 2/3, still CLOSED.", "caido")
    query(6, "Breaker failure 3/3 -> circuit OPENS.", "caido")
    query(7, "Circuit OPEN -> rejected at once (intentos=0, no call made, answers in milliseconds).", "caido")
    query(8, "Circuit OPEN rejects even a healthy request (fail fast).", "normal")

    print()
    wait(RECOVERY_WAIT_SEC, "recovery timeout so the breaker can go HALF_OPEN")
    query(9, "HALF_OPEN trial request fails -> circuit goes back to OPEN.", "caido")

    print()
    wait(RECOVERY_WAIT_SEC, "recovery timeout again")
    query(10, "HALF_OPEN trial request succeeds -> circuit CLOSES. Service recovered.", "normal")


if __name__ == "__main__":
    main()
