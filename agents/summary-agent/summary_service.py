def generate_summary(invoice, risk):
    """
    Generate a concise deterministic invoice summary.
    """

    vendor = invoice.get("vendor", "Unknown vendor")
    invoice_number = invoice.get("invoiceNumber", "Unknown")
    invoice_date = invoice.get("invoiceDate", "Unknown")
    total = invoice.get("total", 0)

    risk_level = risk.get("riskLevel", "UNKNOWN")
    risk_score = risk.get("riskScore", 0)
    flags = risk.get("flags", [])

    summary = (
        f"Invoice {invoice_number} from {vendor}, dated {invoice_date}, "
        f"has a total amount of INR {total:,.2f}. "
        f"The invoice has been assessed as {risk_level} risk "
        f"with a risk score of {risk_score}/100."
    )

    if flags:
        summary += " Risk flags: " + "; ".join(flags) + "."
    else:
        summary += " No risk flags were detected."

    return summary
