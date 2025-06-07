import pdfplumber # extracts texts from text-based pdfs
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
from PIL import Image
import os
import unicodedata
import re


def clean_extracted_text(text: str, lowercase: bool = False) -> str:
    """
    Cleans extracted text by:
    - Normalizing Unicode
    - Fixing broken words across lines
    - Removing non-printable characters
    - Removing special symbols
    - Collapsing whitespace
    - Optionally lowercasing the text
    """

    # normalize Unicode characters (e.g., accented → unaccented)
    text = unicodedata.normalize("NFKC", text)

    # remove non-printable/control characters
    text = ''.join(char for char in text if char.isprintable())

    # fix broken words from line breaks with hyphens (e.g., "devel-\nopment" → "development")
    text = re.sub(r'-\s*\n\s*', '', text)

    # replace all remaining newlines and tabs with a space
    text = re.sub(r'[\r\n\t]+', ' ', text)

    # remove unwanted characters except standard punctuation
    allowed_punctuation = r"\.,;:!?()'\""
    text = re.sub(rf"[^a-zA-Z0-9{allowed_punctuation}\s]", '', text)

    # add space after punctuation if missing (e.g., "Hello.This" → "Hello. This")
    text = re.sub(r'([.,;:!?])([^\s])', r'\1 \2', text)

    # collapse multiple spaces into one
    text = re.sub(r'\s{2,}', ' ', text)

    # trim leading/trailing whitespace
    text = text.strip()

    # optional: convert to lowercase for normalization
    if lowercase:
        text = text.lower()

    return text



def is_scanned_pdf(pdf_path: str) -> bool:
    """Check if the PDF is scanned (i.e., has no extractable text)."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    return False
        return True
    except Exception as e:
        print(f"[ERROR] Failed to check PDF type: {e}")
        return True  # assume scanned if check fails



def preprocess_image_for_ocr(pil_image):
    """
    Converts PIL image to OpenCV format and applies preprocessing to improve OCR accuracy.
    - Converts to grayscale
    - Applies adaptive thresholding
    """
    cv_image = np.array(pil_image.convert('RGB'))  # ensure it's RGB
    gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return Image.fromarray(thresh)



def ocr_pdf_text(pdf_path: str, lang: str = 'eng') -> str:
    """
    Extracts and cleans text from PDF using direct extraction or OCR based on content type.
    Uses pdfplumber if PDF has text layer; otherwise, falls back to OCR.
    """
    try:
        # step 1: check if PDF is scanned
        if not is_scanned_pdf(pdf_path):
            print("[INFO] Using pdfplumber for text extraction...")
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += clean_extracted_text(page_text) + " "
            return text.strip()

        # step 2: fallback to OCR
        print("[INFO] Using OCR for text extraction...")
        text = ""
        images = convert_from_path(pdf_path)

        for idx, image in enumerate(images):
            preprocessed_image = preprocess_image_for_ocr(image)
            raw_text = pytesseract.image_to_string(preprocessed_image, lang=lang)
            cleaned_text = clean_extracted_text(raw_text)
            text += cleaned_text + " "

        return text.strip()

    except Exception as e:
        print(f"[ERROR] Failed to extract text from {pdf_path}: {e}")
        return ""
