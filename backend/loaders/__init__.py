import os

from loaders.pdf_loader import extract_pdf_text
from loaders.image_loader import extract_image_text
from loaders.txt_loader import extract_txt_text


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_pdf_text(file_path)

    if ext == ".txt":
        return extract_txt_text(file_path)

    if ext in [".png", ".jpg", ".jpeg"]:
        return extract_image_text(file_path)

    raise ValueError(f"Unsupported file type: {ext}")
