"""Smoke test for the backend. Run it against any environment to prove it behaves the same.

Usage:  python scripts/check_backend.py [BASE_URL]
Default BASE_URL is http://localhost:8000. Uses only the Python standard library.

Typical use in the Lift-and-Shift exercise:
  python scripts/check_backend.py http://localhost:8000          # on-premise (local Docker)
  python scripts/check_backend.py http://<EC2_PUBLIC_IP>:8000    # AWS (EC2)
"""
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000").rstrip("/")


def call(method: str, path: str, body: dict | None = None) -> tuple[int, dict, float]:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    start = time.monotonic()
    with urllib.request.urlopen(request, timeout=15) as response:
        payload = json.load(response)
        return response.status, payload, (time.monotonic() - start) * 1000


def main() -> int:
    print(f"Target : {BASE_URL}")
    print(f"Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    failures = 0

    checks = [
        ("GET /health", "GET", "/health", None, lambda d: d.get("status") == "healthy"),
        (
            "POST /api/v1/consultar (modo=normal)",
            "POST",
            "/api/v1/consultar",
            {"modo": "normal", "payload": "check-01"},
            lambda d: d.get("estado") == "OK" and d.get("circuito") == "CLOSED",
        ),
    ]
    for label, method, path, body, is_ok in checks:
        try:
            status, payload, ms = call(method, path, body)
            passed = status == 200 and is_ok(payload)
            print(f"[{'PASS' if passed else 'FAIL'}] {label} -> HTTP {status} in {ms:.0f} ms")
            print(f"       {json.dumps(payload, ensure_ascii=False)}")
            failures += 0 if passed else 1
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"[FAIL] {label} -> {exc}")
            failures += 1

    print(f"\nResult: {'ALL CHECKS PASSED' if failures == 0 else f'{failures} CHECK(S) FAILED'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
