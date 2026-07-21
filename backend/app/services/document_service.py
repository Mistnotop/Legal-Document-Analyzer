from pathlib import Path

import fitz
from fastapi import UploadFile
from docx import Document

from app.core.config import (
    ALLOWED_UPLOAD_EXTENSIONS,
    MAX_UPLOAD_SIZE_BYTES,
    UPLOAD_DIR,
)


def extract_text(file) -> str:
    if hasattr(file, "filename") and hasattr(file, "file"):
        return extract_upload(file)

    return extract_text_from_path(Path(file))


def extract_upload(file: UploadFile) -> str:
    if not file.filename:
        raise ValueError("Uploaded file must have a filename")

    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_UPLOAD_EXTENSIONS))
        raise ValueError(f"Unsupported file format. Upload one of: {allowed}")

    if file.size is not None and file.size > MAX_UPLOAD_SIZE_BYTES:
        raise ValueError("File is too large. Maximum upload size is 10 MB.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    file_path = UPLOAD_DIR / Path(file.filename).name
    file.file.seek(0)
    content = file.file.read()

    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise ValueError("File is too large. Maximum upload size is 10 MB.")

    file_path.write_bytes(content)

    try:
        text = extract_text_from_path(file_path)
        if not text.strip():
            raise ValueError("No text could be extracted from this document.")
        return text
    finally:
        file_path.unlink(missing_ok=True)


def extract_text_from_path(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_pdf(file_path)

    if suffix == ".docx":
        return extract_docx(file_path)

    if suffix == ".txt":
        return extract_txt(file_path)

    raise ValueError("Unsupported file format")


def extract_pdf(file_path: Path) -> str:
    text = ""

    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()

    return text


def extract_docx(file_path: Path) -> str:
    document = Document(file_path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def extract_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore")
