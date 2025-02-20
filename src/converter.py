"""
A python module to convert img (jpg, png) to pdf, and pdf to img (jpg, png).
It can also make a pdf out of a list of images and pdfs.

AUTHOR: Marina CHAU
DATE: 2025-02-20

"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pathlib import Path
from loguru import logger
import os
import img2pdf

# -----------------------------
# Decorator to check file format
# -----------------------------
def check_format(valid_formats):
    """Decorator to check the file format before processing."""
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Extract file paths from arguments that are str or Path objects
            file_paths = [arg for arg in args if isinstance(arg, (str, Path))]
            for file_path in file_paths:
                if Path(file_path).suffix.lower() not in valid_formats:
                    logger.error(f"Invalid file format: {file_path}")
                    return False  # Stop execution if an invalid format is found
            return func(self, *args, **kwargs)  # Proceed if all formats are valid
        return wrapper
    return decorator

# -----------------------------
# Converter class
# -----------------------------
class Converter:
    def __init__(self):
        # You can change this output directory as needed
        self.output_dir = '/home/nvidia/Documents/private_projects/MakeItPrivate/Data/output_converter'
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
    @check_format(valid_formats={'.jpg', '.png'})
    def img_to_pdf(self, img_paths: List[str], pdf_path: str):
        """
        Convert images (jpg, png) to a PDF file.
        Handles both single and multiple images.

        Args:
            img_paths (List[str]): List of image file paths.
            pdf_path (str): Full path (including filename) for the output PDF.
        """
        if not img_paths:
            logger.error("No image file provided.")
            return False
        
        logger.info(f"Converting {img_paths} to PDF at {pdf_path}")
        try:
            # For both single and multiple images, img2pdf.convert accepts a list of Paths.
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert([Path(img) for img in img_paths]))
            logger.info(f"PDF file created successfully: {pdf_path}")
            return pdf_path
        except Exception as e:
            logger.error(f"Error during conversion: {e}")
            return False

# -----------------------------
# FastAPI app definition
# -----------------------------
app = FastAPI()
converter = Converter()

class UserInput(BaseModel):
    img_path: List[str]
    pdf_path: str

@app.post("/converter")
def convert_to_pdf(input: UserInput):
    """
    Endpoint to convert one or more images to a PDF file.
    Expects a JSON payload with:
      - img_path: a list of image file paths (strings)
      - pdf_path: the full path for the output PDF file
    """
    result = converter.img_to_pdf(input.img_path, input.pdf_path)
    return {"result": result}
