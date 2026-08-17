import re
from typing import Any, Dict


def _extract(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)

    if match:
        return match.group(1).strip()

    return None


def _extract_amount(pattern: str, text: str) -> float | None:
    value = _extract(pattern, text)

    if not value:
        return None

    try:
        return float(value.replace(",", ""))
    except ValueError:
        return None


def parse_invoice(text: str) -> Dict[str, Any]:
    """
    Convert raw OCR invoice text into structured invoice information.
    """

    invoice_number = _extract(
        r"Invoice\s+Number\s*[:=]+\s*([A-Z0-9\-]+)",
        text
    )

    invoice_date = _extract(
        r"Invoice\s+Date\s*[:=]\s*([0-9]{2}-[0-9]{2}-[0-9]{4})",
        text
    )

    due_date = _extract(
        r"Due\s+Date\s*[:=]\s*([0-9]{2}-[0-9]{2}-[0-9]{4})",
        text
    )

    po_number = _extract(
        r"PO\s+Number\s*[:=]\s*([A-Z0-9\-]+)",
        text
    )

    gstin = _extract(
        r"GSTIN\s*:\s*([A-Z0-9]+)",
        text
    )

    subtotal = _extract_amount(
        r"SUBTOTAL\s+([0-9,]+\.[0-9]{2})",
        text
    )

    gst = _extract_amount(
        r"GST\s*\([^)]*\)\s+([0-9,]+\.[0-9]{2})",
        text
    )

    total = _extract_amount(
        r"TOTAL\s*\([^)]*\)\s+([0-9,]+\.[0-9]{2})",
        text
    )

    # Vendor is the text appearing before the first address.
    vendor = None

    vendor_match = re.search(
        r"^\s*([A-Z][A-Z\s&]+)\s*$",
        text,
        re.MULTILINE
    )

    if vendor_match:
        vendor = vendor_match.group(1).strip()

    return {
        "invoiceNumber": invoice_number,
        "invoiceDate": invoice_date,
        "dueDate": due_date,
        "poNumber": po_number,
        "vendor": vendor,
        "gstin": gstin,
        "subtotal": subtotal,
        "gst": gst,
        "total": total,
    }