from ocr_service import extract_text
from invoice_parser import parse_invoice


image_path = "test_data/test_invoice.png"

text, _ = extract_text(image_path)

invoice = parse_invoice(text)

print("\n===== STRUCTURED INVOICE =====")

for key, value in invoice.items():
    print(f"{key}: {value}")