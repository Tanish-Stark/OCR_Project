import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import cv2
import numpy as np

# Set language codes (hin = Hindi, mar = Marathi, eng = English)
LANGS = "hin+mar+eng"

# Path to your PDF
pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")

# Output directory for images
output_dir = "temp_images"
os.makedirs(output_dir, exist_ok=True)

# Convert PDF to images (1 image per page)
images = convert_from_path(pdf_path, dpi=300, output_folder=output_dir)

# Helper: Preprocess PIL image using OpenCV
def preprocess_image(pil_image):
    img = np.array(pil_image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)
    return Image.fromarray(denoised)

# Extract text from each image
full_text = ""
for i, image in enumerate(images):
    preprocessed = preprocess_image(image)
    text = pytesseract.image_to_string(preprocessed, lang=LANGS)
    full_text += f"\n--- Page {i + 1} ---\n{text}"

# Save extracted text
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("✅ Text extraction complete. Check 'extracted_text.txt'")
