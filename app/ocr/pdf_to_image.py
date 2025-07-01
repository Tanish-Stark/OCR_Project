import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import cv2
import numpy as np

# Set language codes (hin = Hindi, mar = Marathi, eng = English)
LANGS = "hin+mar+eng"
TESS_CONFIG = r'--oem 3 --psm 6'

# Path to your PDF
pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")

# Output directories
output_dir = "temp_images"
os.makedirs(output_dir, exist_ok=True)

debug_dir = "debug_images"
os.makedirs(debug_dir, exist_ok=True)

# Convert PDF to images (1 image per page)
images = convert_from_path(pdf_path, dpi=300, output_folder=output_dir)
print(f"📄 Converted {len(images)} pages from PDF.")

# Preprocessing variants: OTSU + CLAHE
def preprocess_image_variants(pil_image, page_num):
    img = np.array(pil_image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # OTSU Binarization
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)

    # Save debug images
    Image.fromarray(otsu).save(os.path.join(debug_dir, f"page_{page_num}_otsu.png"))
    Image.fromarray(clahe_img).save(os.path.join(debug_dir, f"page_{page_num}_clahe.png"))

    return {
        "otsu": Image.fromarray(otsu),
        "clahe": Image.fromarray(clahe_img)
    }

# Extract text from each preprocessed image variant
full_text = ""
for i, image in enumerate(images):
    page_num = i + 1
    print(f"🔍 Processing page {page_num}...")

    variants = preprocess_image_variants(image, page_num)

    for variant_name, pre_img in variants.items():
        text = pytesseract.image_to_string(pre_img, lang=LANGS, config=TESS_CONFIG)
        full_text += f"\n--- Page {page_num} ({variant_name}) ---\n{text}"
        print(f"✅ OCR complete for Page {page_num} ({variant_name})")

# Save the full extracted text
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print("✅ Text extraction complete. Check 'extracted_text.txt' and debug images in 'debug_images/'")
