"""Load balancer check: sends several requests through the proxy / API Gateway
and counts which backend instance answered each one.

Usage: python scripts/check_proxy.py [BASE_URL] [REQUESTS]
Default BASE_URL is http://localhost:8080 and REQUESTS is 6.
Exit code 0 when every request succeeded, 1 otherwise.
"""
import json
import sys
import urllib.request
from collections import Counter

BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080").rstrip("/")
TOTAL = int(sys.argv[2]) if len(sys.argv) > 2 else 6


def post(path: str, body: dict) -> dict:
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main() -> int:
    print(f"Target : {BASE_URL}")
    print(f"Sending {TOTAL} requests\n")
    served = Counter()
    failures = 0
    for i in range(1, TOTAL + 1):
        try:
            data = post("/api/v1/consultar", {"modo": "normal", "payload": f"req-{i}"})
            instance = data.get("instancia", "?")
            served[instance] += 1
            print(f"[PASS] request {i}: estado={data.get('estado')} answered by {instance}")
        except Exception as exc:  # noqa: BLE001 - smoke test, report any error
            failures += 1
            print(f"[FAIL] request {i}: {exc}")

    print("\nRequests per backend:")
    for instance, count in sorted(served.items()):
        print(f"  {instance}: {count}")
    ok = failures == 0
    print("\nResult:", "ALL REQUESTS OK" if ok else f"{failures} REQUEST(S) FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
