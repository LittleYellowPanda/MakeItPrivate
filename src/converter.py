"""
A python module to convert img (jpg, png) to pdf, and pdf to img (jpg, png).
It can also make a pdf out of a list of images and pdfs.

AUTHOR: Marina CHAU
DATE: 2025-02-20

"""
from pydantic import BaseModel
from typing import List
from pathlib import Path
from loguru import logger
import os
from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil

from fastapi import FastAPI, UploadFile, File
from typing import List
from pathlib import Path
from loguru import logger
import os
import img2pdf
import shutil

from PyPDF2 import PdfWriter
from typing import List

# -----------------------------
# FastAPI app definition
# -----------------------------
app = FastAPI()

# Output directory for storing uploaded images and PDFs
OUTPUT_DIR = "/home/pcbanc/Documents/Projects/MakeItPrivate/Data/output_converter"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# File format checker
# -----------------------------
VALID_FORMATS = {".jpg", ".png"}
VALID_PDF_FORMATS = {".pdf"}

def is_valid_format(file_name: str) -> bool:
    """Check if the uploaded file is in an allowed format."""
    return Path(file_name).suffix.lower() in VALID_FORMATS

def is_valid_pdf_format(file_name: str) -> bool:
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

    for file in files:
        if not is_valid_format(file.filename):
            return {"error": f"Invalid file format: {file.filename}"}

        file_path = os.path.join(OUTPUT_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        image_paths.append(file_path)

    if not image_paths:
        return {"error": "No valid image files provided."}

    # Define output PDF path
    output_pdf = os.path.join(OUTPUT_DIR, "output.pdf")

    try:
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert([Path(img) for img in image_paths]))
        logger.info(f"PDF file created successfully: {output_pdf}")
        return {"message": "PDF created successfully", "pdf_path": output_pdf}
    except Exception as e:
        logger.error(f"Error during conversion: {e}")
        return {"error": "Failed to create PDF"}
    
# -----------------------------
# PDF merger
# -----------------------------
@app.post("/merge/")
def merge_pdfs(files: List[UploadFile] = File(...)):
    """
    Accepts multiple PDF files, saves them, and merges them into one PDF.
    """
    pdf_paths = []
    merger = PdfWriter()
    
    for file in files:
        if not is_valid_pdf_format(file.filename):
            return {"error": f"Invalid file format: {file.filename}"}
        file_path = os.path.join(OUTPUT_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        merger.append(file_path)

    if not merger:
        return {"error": "No valid PDF files provided."}

    # Define output merged PDF path
    merged_pdf = os.path.join(OUTPUT_DIR, "merged.pdf")
    
    # TODO: Call your merge_pdfs function and capture its return value
    try:
        with open(merged_pdf, "wb") as f:
            merger.write(f)
            return {"message": "Merged PDF created successfully", "pdf_path": merged_pdf}
    except Exception as e:
        return {"error": f"Failed to merge PDFs: {e}"}