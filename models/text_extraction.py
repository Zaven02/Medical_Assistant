import pdfplumber
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(('.png', '.jpeg', '.jpg')):
        return extract_text_from_image(file_path, lang='rus')
    else:
        print(f"Unsupported file type: {file_path}")
        return None

def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    print(f"Warning: No text found on page {page.page_number}")
            return text.strip()  # Return trimmed text to remove unnecessary whitespace
    except Exception as e:
        print(f"Error reading PDF file '{file_path}': {e}")
        return None

def extract_text_from_image(file_path, lang='rus'):
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()  # Return trimmed text to remove unnecessary whitespace
    except Exception as e:
        print(f"Error extracting text from image '{file_path}': {e}")
        return None
