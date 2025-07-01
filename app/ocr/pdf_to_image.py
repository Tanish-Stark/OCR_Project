from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_dir, dpi=300):
    os.makedirs(output_dir, exist_ok=True)
    images = convert_from_path(pdf_path, dpi=dpi, output_folder=output_dir)
    return images
