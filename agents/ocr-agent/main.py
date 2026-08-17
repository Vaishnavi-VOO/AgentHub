import time
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from ocr_service import extract_text
from invoice_parser import parse_invoice


app = FastAPI(
    title="AgentHub OCR Agent",
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
        "agentId": "ocr-001",
        "agentName": "OCR Agent",
        "status": "running"
    }


@app.post("/invoke")
def invoke(request: InvokeRequest):
    start_time = time.perf_counter()

    image_path = request.input.get("imagePath")

    # Validate input
    if not image_path:
        return {
            "success": False,
            "requestId": request.requestId,
            "error": {
                "code": "INVALID_INPUT",
                "message": "imagePath is required in input"
            }
        }

    try:
        # Step 1: Extract raw text using Tesseract
        text, _ = extract_text(image_path)

        # Step 2: Convert OCR text into structured invoice data
        invoice = parse_invoice(text)

        # Step 3: Calculate total processing time
        processing_time = (
            time.perf_counter() - start_time
        ) * 1000

        # Step 4: Return response using the shared AgentHub contract
        return {
            "success": True,
            "requestId": request.requestId,
            "result": {
                "text": text,
                "invoice": invoice
            },
            "metadata": {
                "processingTime": round(processing_time, 2),
                "agentVersion": "1.0"
            }
        }

    except FileNotFoundError:
        return {
            "success": False,
            "requestId": request.requestId,
            "error": {
                "code": "FILE_NOT_FOUND",
                "message": "The specified image file was not found"
            }
        }

    except ValueError as error:
        return {
            "success": False,
            "requestId": request.requestId,
            "error": {
                "code": "PROCESSING_ERROR",
                "message": str(error)
            }
        }

    except Exception:
        return {
            "success": False,
            "requestId": request.requestId,
            "error": {
                "code": "PROCESSING_ERROR",
                "message": "Unable to process the invoice"
            }
        }