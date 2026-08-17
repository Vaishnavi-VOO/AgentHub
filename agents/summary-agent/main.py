import time
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from summary_service import generate_summary


app = FastAPI(
    title="AgentHub Summary Agent",
    version="1.0"
)


class InvokeRequest(BaseModel):
    requestId: str
    input: Dict[str, Any]
    context: Dict[str, Any]


@app.get("/")
def health_check():
    return {
        "success": True,
        "agentId": "summary-001",
        "agentName": "Summary Agent",
        "status": "running"
    }


@app.post("/invoke")
def invoke(request: InvokeRequest):
    start_time = time.perf_counter()

    invoice = request.input.get("invoice")
    risk = request.input.get("risk", {})

    if not invoice:
        return {
            "success": False,
            "requestId": request.requestId,
            "error": {
                "code": "INVALID_INPUT",
                "message": "invoice is required in input"
            }
        }

    try:
        summary = generate_summary(invoice, risk)

        processing_time = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "success": True,
            "requestId": request.requestId,
            "result": {
                "summary": summary
            },
            "metadata": {
                "processingTime": round(processing_time, 2),
                "agentVersion": "1.0"
            }
        }

    except Exception:
        return {
            "success": False,
            "requestId": request.requestId,
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "Unable to generate invoice summary"
            }
        }