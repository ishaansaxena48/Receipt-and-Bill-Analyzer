import os
import re
from PIL import Image, ImageFilter
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()

        elif ext == ".pdf":
            images = convert_from_path(filepath, poppler_path=POPPLER_PATH)
            return "\n".join([pytesseract.image_to_string(img) for img in images])

        elif ext in [".jpg", ".jpeg", ".png"]:
            image = Image.open(filepath).convert("L")  # Grayscale
            image = image.point(lambda x: 0 if x < 150 else 255)  # Binarize
            image = image.filter(ImageFilter.SHARPEN)  # Sharpen text
            return pytesseract.image_to_string(image)

        else:
            return "Unsupported file format."

    except Exception as e:
        return f"[ERROR] {e}"

def parse_receipt(text):
    lines = text.strip().split('\n')

    vendor = "Unknown"
    date = "Unknown"
    amount = 0.0
    currency = "INR"

    for line in lines:
        line_clean = line.strip()

        if line_clean.lower().startswith("vendor:"):
            vendor = line_clean.split(":", 1)[1].strip().title()

        elif line_clean.lower().startswith("date:"):
            date = line_clean.split(":", 1)[1].strip()

        elif "total amount" in line_clean.lower():
            if "rs" in line_clean.lower() or "₹" in line_clean:
                currency = "INR"
            elif "$" in line_clean:
                currency = "USD"

            match = re.search(r"(\d{1,3}(?:[,\d{3}]*)(?:\.\d{1,2})?)", line_clean)
            if match:
                try:
                    amount = float(match.group(1).replace(",", ""))
                except ValueError:
                    amount = 0.0

    return {
        "vendor": vendor,
        "date": date,
        "amount": amount,
        "currency": currency
    }