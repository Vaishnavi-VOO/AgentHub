import time
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from fraud_service import analyze_invoice


app = FastAPI(
    title="AgentHub Fraud Agent",
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
        "agentId": "fraud-001",
        "agentName": "Fraud Agent",
        "status": "running"
    }


@app.post("/invoke")
def invoke(request: InvokeRequest):
    start_time = time.perf_counter()

    invoice = request.input.get("invoice")

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
        risk_analysis = analyze_invoice(invoice)

        processing_time = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "success": True,
            "requestId": request.requestId,
            "result": {
                "risk": risk_analysis
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
                "message": "Unable to analyze invoice"
            }
        }