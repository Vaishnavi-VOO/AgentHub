from ocr_service import extract_text


image_path = "test_data/test_invoice.png"

text, processing_time = extract_text(image_path)

print("\n===== OCR RESULT =====")
print(text)

print("\n===== PROCESSING TIME =====")
print(f"{processing_time} ms")