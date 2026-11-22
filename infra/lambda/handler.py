import json
from datetime import datetime, timezone


def lambda_handler(event: dict, context: object) -> dict:
    """Decoupled serverless event processor for resilience audit logs."""
    payload = event if isinstance(event, dict) else {}
    record = {
        "event_type": payload.get("evento", "resilience_event"),
        "mode": payload.get("modo", "unknown"),
        "status": payload.get("estado", "unknown"),
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Audit event processed", "record": record}),
    }
