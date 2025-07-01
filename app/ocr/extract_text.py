import pytesseract
from PIL import Image

def extract_text_from_images(images, langs="hin+mar+eng"):
    full_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang=langs)
        full_text += f"\n--- Page {i + 1} ---\n{text}"
    return full_text
