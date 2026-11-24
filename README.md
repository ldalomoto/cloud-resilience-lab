# Circuit Breaker and Timeout Patterns / Patrones Circuit Breaker y Timeout

[English](#english) | [Español](#español)

---

## English

### What this practice is about
This exercise shows two resilience patterns working together in a FastAPI backend:

- **Timeout:** a request to a downstream service is cut off after 1 second, so a slow dependency cannot block the system.
- **Retry with exponential backoff:** a failed call is retried up to 2 times, waiting 0.5 s, then 1 s.
- **Circuit Breaker:** after 3 failed requests the circuit opens (`OPEN`) and further calls fail immediately, without waiting. After 10 seconds it lets one test call through (`HALF_OPEN`). If it succeeds, the circuit closes again (`CLOSED`).

The backend exposes `POST /api/v1/consultar` with three modes: `normal` (answers fast), `lento` (slower than the timeout) and `caido` (always fails).

### Where is everything
| What | Where |
|---|---|
| Full explanation, diagrams, configuration and reproduction steps | [`docs/circuit-breaker-and-timeout.md`](docs/circuit-breaker-and-timeout.md) |
| Circuit Breaker, retry and timeout source code | `app/backend/src/` (`circuit_breaker.py`, `retry_policy.py`, `resilience_service.py`, `downstream_client.py`) |
| Unit tests (20 tests) | `app/backend/tests/` (`test_circuit_breaker.py`, `test_timeout.py`, `test_resilience_service.py`) |
| Live demo script | [`scripts/demo_circuit_breaker.py`](scripts/demo_circuit_breaker.py) |
| Evidence | [`docs/evidence/circuit-breaker-timeout/`](docs/evidence/circuit-breaker-timeout/) |

### Evidence
| File | What it shows |
|---|---|
| `unit-tests-output.txt` | The 20 unit tests passing |
| `live-demo-output.txt` | The 10-step live demo against the running backend |
| `backend-server-log.txt` | Server log recorded during the demo |
| `01-normal-ok.png` | `normal` mode answers correctly, circuit `CLOSED` |
| `02-slow-timeout-error.png` | `lento` mode is cut off by the timeout |
| `03-down-first-failure.png` | `caido` mode: first failure |
| `04-down-circuit-opens.png` | Failures accumulate and the circuit opens |
| `05-circuit-open-fail-fast.png` | With the circuit `OPEN`, requests fail instantly |
| `06-circuit-recovered.png` | After the recovery time, the circuit closes again |
| `07-docker-containers-running.png` | Containers running in Docker Desktop |

### How to reproduce
The exact commands (run the tests, start the backend with Docker Compose, run the demo) are in section 4 of [`docs/circuit-breaker-and-timeout.md`](docs/circuit-breaker-and-timeout.md).

---
