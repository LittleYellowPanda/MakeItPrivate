import streamlit as st
import requests
import os
import time  # Add a small delay to allow the file to be written

API_URL = "http://fastapi:8000/upload/"
API_URL_PDF_MERGER = "http://fastapi:8000/merge/"
SHARED_DIR = "/app/shared/"  # Ensure Streamlit and FastAPI use the same volume

st.title("🖼️ Image to PDF Converter - CHAU Family")

uploaded_files = st.file_uploader("Upload JPG or PNG images", type=["jpg", "png"], accept_multiple_files=True)

if st.button("Convert to PDF"):
    if not uploaded_files:
        st.error("Please upload at least one image.")
    else:
        files_to_send = [("files", (file.name, file, file.type)) for file in uploaded_files]

        with st.spinner("Converting... ⏳"):
            response = requests.post(API_URL, files=files_to_send)

        if response.status_code == 200:
            result = response.json()
            pdf_filename = "output.pdf"
            pdf_path = os.path.join(SHARED_DIR, pdf_filename)

            # Wait for the file to be written
            time.sleep(1)

            if os.path.exists(pdf_path):  # ✅ Double-check that the file exists before offering download
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                st.success("Conversion successful! Click to download your PDF.")
            else:
                st.error("PDF file not found. Please try again.")
        else:
            st.error("Error processing your request.")

st.title("\U0001F4D1 PDF Merger")

uploaded_files_pdf = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if st.button("Merge PDF"):
    if not uploaded_files_pdf:
        st.error("Please upload at least one image.")
    else:
        files_to_send = [("files", (file.name, file, file.type)) for file in uploaded_files_pdf]

        with st.spinner("Merging... ⏳"):
            response = requests.post(API_URL_PDF_MERGER, files=files_to_send)

        if response.status_code == 200:
            result = response.json()
            pdf_filename = "merged.pdf"
            pdf_path = os.path.join(SHARED_DIR, pdf_filename)

            # Wait for the file to be written
            time.sleep(1)

            if os.path.exists(pdf_path):  # ✅ Ensure file is there before download
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Merged PDF",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                st.success("Merging successful! Click to download your PDF.")
            else:
                st.error("Merged PDF file not found. Please try again.")
        else:
            st.error("Error processing your request.")
