from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from src.circuit_breaker import CircuitBreaker
from src.config import CONFIG
from src.resilience_service import ResilienceService

app = FastAPI(title="Cloud Resilience Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

breaker = CircuitBreaker(
    failure_threshold=CONFIG.failure_threshold,
    recovery_timeout_sec=CONFIG.recovery_timeout_sec,
)
service = ResilienceService(config=CONFIG, breaker=breaker)


class QueryRequest(BaseModel):
    modo: str = Field(default="normal", pattern="^(normal|lento|caido)$")
    payload: str = Field(default="sample-payload", min_length=1)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy", "instance": CONFIG.instance_id}


@app.post("/api/v1/consultar")
async def consultar(req: QueryRequest) -> dict[str, object]:
    outcome = await service.process_query(mode=req.modo)
    return {
        "estado": outcome.status,
        "intentos": outcome.attempts,
        "circuito": outcome.circuit_state,
        "instancia": outcome.instance_id,
        "detalle": outcome.detail,
    }
