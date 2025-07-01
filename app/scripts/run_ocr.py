from app.ocr.pdf_to_images import pdf_to_images
from app.ocr.extract_text import extract_text_from_images
from app.storage.db import insert_document
import sys, os

pdf_path = sys.argv[1]
filename = os.path.basename(pdf_path)
output_dir = "data/images"
text_path = f"data/extracted_texts/{filename}.txt"

# 1. OCR
images = pdf_to_images(pdf_path, output_dir)
text = extract_text_from_images(images)
num_pages = len(images)

# 2. Save text to file
os.makedirs("data/extracted_texts", exist_ok=True)
with open(text_path, "w", encoding="utf-8") as f:
    f.write(text)

# 3. Store in DB
insert_document(
    filename=filename,
    text=text,
    language="hin+mar+eng",  # static for now, can use detection later
    num_pages=num_pages,
    doc_type=None,
    filepath=pdf_path
)

print(f"✅ Stored {filename} in DB with {num_pages} pages")
