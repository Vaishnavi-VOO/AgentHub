def analyze_invoice(invoice):
    """
    Perform deterministic rule-based invoice risk analysis.
    """

    risk_score = 0
    risk_flags = []

    # Rule 1: Missing invoice number
    if not invoice.get("invoiceNumber"):
        risk_score += 20
        risk_flags.append("Missing invoice number")

    # Rule 2: Missing invoice date
    if not invoice.get("invoiceDate"):
        risk_score += 15
        risk_flags.append("Missing invoice date")

    # Rule 3: Missing vendor
    if not invoice.get("vendor"):
        risk_score += 20
        risk_flags.append("Missing vendor information")

    # Rule 4: Missing GSTIN
    if not invoice.get("gstin"):
        risk_score += 20
        risk_flags.append("Missing GSTIN")

    # Rule 5: Invalid total
    total = invoice.get("total")

    if total is None:
        risk_score += 20
        risk_flags.append("Missing invoice total")
    elif total <= 0:
        risk_score += 30
        risk_flags.append("Invalid invoice total")

    # Rule 6: Check subtotal + GST against total
    subtotal = invoice.get("subtotal")
    gst = invoice.get("gst")

    if subtotal is not None and gst is not None and total is not None:
        calculated_total = round(subtotal + gst, 2)

        if abs(calculated_total - total) > 1:
            risk_score += 30
            risk_flags.append("Subtotal + GST does not match total")

    # Keep score within 0–100
    risk_score = min(risk_score, 100)

    # Determine risk level
    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "flags": risk_flags
    }