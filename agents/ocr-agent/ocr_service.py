import os
import time

import cv2
import pytesseract


def extract_text(image_path: str) -> tuple[str, float]:
    """
    Extract text from an invoice image using Tesseract OCR.

    Returns:
        tuple[str, float]:
            extracted text and processing time in milliseconds.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    start_time = time.perf_counter()

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read the image.")

    # Convert to grayscale to improve OCR consistency.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    processing_time = (time.perf_counter() - start_time) * 1000

    return text.strip(), round(processing_time, 2)