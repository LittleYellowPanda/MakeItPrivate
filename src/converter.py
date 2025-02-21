"""
A Python module to convert images (JPG, PNG) to PDF and extract images from PDFs.
It can also merge multiple PDFs into one.

AUTHOR: Marina CHAU
DATE: 2025-02-20
"""

from fastapi import FastAPI, UploadFile, File
from typing import List
from pathlib import Path
import os
import shutil
import img2pdf
from PyPDF2 import PdfWriter
from loguru import logger

# -----------------------------
# FastAPI app definition
# -----------------------------
app = FastAPI()

# Shared directory for storing uploaded files and output PDFs
SHARED_DIR = "/app/shared/"
os.makedirs(SHARED_DIR, exist_ok=True)

# -----------------------------
# File format validation
# -----------------------------
VALID_IMAGE_FORMATS = {".jpg", ".png"}
VALID_PDF_FORMATS = {".pdf"}

def is_valid_image(file_name: str) -> bool:
    """Check if the uploaded file is an allowed image format."""
    return Path(file_name).suffix.lower() in VALID_IMAGE_FORMATS

def is_valid_pdf(file_name: str) -> bool:
    """Check if the uploaded file is a PDF."""
    return Path(file_name).suffix.lower() in VALID_PDF_FORMATS

# -----------------------------
# Image to PDF conversion
# -----------------------------
@app.post("/upload/")
async def upload_and_convert(files: List[UploadFile] = File(...)):
    """
    Accepts multiple image files, saves them, and converts them into a PDF.
    """
    image_paths = []
    output_pdf = os.path.join(SHARED_DIR, "output.pdf")

    for file in files:
        if not is_valid_image(file.filename):
            return {"error": f"Invalid file format: {file.filename}"}

        file_path = os.path.join(SHARED_DIR, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_paths.append(file_path)
        except Exception as e:
            logger.error(f"Error saving file {file.filename}: {e}")
            return {"error": f"Failed to save file: {file.filename}"}

    if not image_paths:
        return {"error": "No valid image files provided."}

    try:
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(image_paths))
        logger.info(f"PDF file created successfully: {output_pdf}")
        return {"message": "PDF created successfully", "pdf_path": output_pdf}
    except Exception as e:
        logger.error(f"Error during PDF conversion: {e}")
        return {"error": "Failed to create PDF"}

# -----------------------------
# PDF merger
# -----------------------------
@app.post("/merge/")
async def merge_pdfs(files: List[UploadFile] = File(...)):
    """
    Accepts multiple PDF files, saves them, and merges them into a single PDF.
    """
    pdf_paths = []
    merged_pdf = os.path.join(SHARED_DIR, "merged.pdf")
    merger = PdfWriter()

    for file in files:
        if not is_valid_pdf(file.filename):
            return {"error": f"Invalid file format: {file.filename}"}
        
        file_path = os.path.join(SHARED_DIR, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            merger.append(file_path)
            pdf_paths.append(file_path)
        except Exception as e:
            logger.error(f"Error saving file {file.filename}: {e}")
            return {"error": f"Failed to save file: {file.filename}"}

    if not pdf_paths:
        return {"error": "No valid PDF files provided."}

    try:
        with open(merged_pdf, "wb") as f:
            merger.write(f)
        logger.info(f"Merged PDF created successfully: {merged_pdf}")
        return {"message": "Merged PDF created successfully", "pdf_path": merged_pdf}
    except Exception as e:
        logger.error(f"Error merging PDFs: {e}")
        return {"error": "Failed to merge PDFs"}
