import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image):
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = image
    text = pytesseract.image_to_string(img, lang='eng+rus')
    return text