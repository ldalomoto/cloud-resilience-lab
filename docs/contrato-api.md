# Contrato de Comunicacion

- Frontend: http://localhost:5173
- Proxy/LB: http://localhost:8080
- Backend: http://localhost:8000

Endpoint principal: POST /api/v1/consultar

Request:
{"modo": "normal", "payload": "test-01"}

Modos: normal | lento | caido

Response:
{"estado": "OK", "intentos": 1, "circuito": "CLOSED", "detalle": "ok"}

Estados: OK | RETRY_OK | TIMEOUT_ERROR | CIRCUIT_OPEN
Circuitos: CLOSED | OPEN | HALF_OPEN
