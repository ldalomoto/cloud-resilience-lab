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

## Español

### En qué consiste la práctica
Este ejercicio muestra dos patrones de resiliencia trabajando juntos en un backend FastAPI:

- **Timeout:** una llamada a un servicio dependiente se corta tras 1 segundo, para que una dependencia lenta no bloquee el sistema.
- **Reintentos con backoff exponencial:** una llamada fallida se reintenta hasta 2 veces, esperando 0,5 s y luego 1 s.
- **Circuit Breaker:** tras 3 peticiones fallidas el circuito se abre (`OPEN`) y las siguientes llamadas fallan al instante, sin esperar. A los 10 segundos deja pasar una llamada de prueba (`HALF_OPEN`). Si funciona, el circuito se cierra de nuevo (`CLOSED`).

El backend expone `POST /api/v1/consultar` con tres modos: `normal` (responde rápido), `lento` (más lento que el timeout) y `caido` (siempre falla).

### Dónde está cada cosa
| Qué | Dónde |
|---|---|
| Explicación completa, diagramas, configuración y pasos para reproducir | [`docs/circuit-breaker-and-timeout.md`](docs/circuit-breaker-and-timeout.md) |
| Código de Circuit Breaker, reintentos y timeout | `app/backend/src/` (`circuit_breaker.py`, `retry_policy.py`, `resilience_service.py`, `downstream_client.py`) |
| Pruebas unitarias (20 pruebas) | `app/backend/tests/` (`test_circuit_breaker.py`, `test_timeout.py`, `test_resilience_service.py`) |
| Script de demostración en vivo | [`scripts/demo_circuit_breaker.py`](scripts/demo_circuit_breaker.py) |
| Evidencias | [`docs/evidence/circuit-breaker-timeout/`](docs/evidence/circuit-breaker-timeout/) |

### Evidencias
| Archivo | Qué muestra |
|---|---|
| `unit-tests-output.txt` | Las 20 pruebas unitarias aprobadas |
| `live-demo-output.txt` | La demostración en vivo de 10 pasos contra el backend |
| `backend-server-log.txt` | Registro del servidor durante la demostración |
| `01-normal-ok.png` | Modo `normal` responde bien, circuito `CLOSED` |
| `02-slow-timeout-error.png` | El modo `lento` es cortado por el timeout |
| `03-down-first-failure.png` | Modo `caido`: primer fallo |
| `04-down-circuit-opens.png` | Los fallos se acumulan y el circuito se abre |
| `05-circuit-open-fail-fast.png` | Con el circuito `OPEN`, las peticiones fallan al instante |
| `06-circuit-recovered.png` | Tras el tiempo de recuperación, el circuito se cierra |
| `07-docker-containers-running.png` | Contenedores corriendo en Docker Desktop |

### Cómo reproducirlo
Los comandos exactos (ejecutar las pruebas, levantar el backend con Docker Compose y correr la demostración) están en la sección 4 de [`docs/circuit-breaker-and-timeout.md`](docs/circuit-breaker-and-timeout.md).
