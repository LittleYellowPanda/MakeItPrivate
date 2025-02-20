import streamlit as st
import requests
import os

# FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/upload/"
API_URL_PDF_MERGER = "http://127.0.0.1:8000/merge/"

st.title("🖼️ Image to PDF Converter - CHAU Family")

# File uploader widget (accepts multiple files)
uploaded_files = st.file_uploader(
    "Upload JPG or PNG images", 
    type=["jpg", "png"], 
    accept_multiple_files=True
)

# Convert button
if st.button("Convert to PDF"):
    if not uploaded_files:
        st.error("Please upload at least one image.")
    else:
        files_to_send = [
            ("files", (file.name, file, file.type))
            for file in uploaded_files
        ]
        
        with st.spinner("Converting... ⏳"):
            response = requests.post(API_URL, files=files_to_send)
        
        if response.status_code == 200:
            result = response.json()
            pdf_path = result.get("pdf_path")

            if pdf_path:
                # Download the PDF
                pdf_filename = os.path.basename(pdf_path)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                st.success("Conversion successful! Click to download your PDF.")
            else:
                st.error("Conversion failed. Please try again.")
        else:
            st.error("Error processing your request.")

st.title("\U0001F4D1 PDF Merger")

# File uploader widget (accepts multiple files)
uploaded_files_pdf = st.file_uploader(
    "Upload PDFs", 
    type=["pdf"], 
    accept_multiple_files=True
)

# Convert button
if st.button("Merge PDF"):
    if not uploaded_files_pdf:
        st.error("Please upload at least one image.")
    else:
        files_to_send = [
            ("files", (file.name, file, file.type))
            for file in uploaded_files_pdf
        ]

        with st.spinner("Converting... ⏳"):
            response = requests.post(API_URL_PDF_MERGER, files=files_to_send)
    
        if response.status_code == 200:
            result = response.json()
            pdf_path = result.get("pdf_path")
            if pdf_path:
                # Download the PDF
                pdf_filename = os.path.basename(pdf_path)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_file,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
                st.success("Merging successful! Click to download your PDF.")
            else:
                st.error("Merging failed. Please try again.")
        else:
            st.error("Error processing your request.")

