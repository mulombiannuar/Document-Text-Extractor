# 📄 Document Text Extractor

**Document Text Extractor** is a Flask-based machine learning project designed to extract, clean, and format text from uploaded PDF documents — whether scanned (image-based) or standard (text-based). It leverages Optical Character Recognition (OCR) and text processing techniques to deliver high-quality, structured text output.

---

## 🚀 Features

- 📤 Upload scanned or regular PDF documents
- 🧠 ML-based OCR for accurate text recognition from images
- 🧹 Text cleaning and formatting
- 🗃 Simple web interface for uploading files
- ⚡ REST API for integration

---

## 🧰 Tech Stack

- **Python 3.8+**
- **Flask** (Web Framework)
- **Tesseract OCR** (for scanned PDFs)
- **PyMuPDF** / **pdfminer.six** (for native PDF text extraction)
- **Pillow / OpenCV** (for image processing)
- **scikit-learn / NLTK** (optional for text cleaning, NLP tasks)

---

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/document-text-extractor.git
cd document-text-extractor
