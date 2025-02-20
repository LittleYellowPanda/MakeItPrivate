# MakeItPrivate

MakeItPrivate is a Python-based application that converts images (JPG, PNG) to PDF and vice versa. It also allows creating a PDF from a list of images and PDFs. The application uses FastAPI for the backend and Streamlit for the frontend.

## Features

- Convert images (JPG, PNG) to PDF
- Convert PDF to images (JPG, PNG)
- Create a PDF from a list of images and PDFs

## Requirements

- Python 3.10
- Docker
- Docker Compose

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/LittleYellowPanda/MakeItPrivate.git
    cd MakeItPrivate
    ```

2. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

## Usage

1. Open your web browser and navigate to `http://localhost:8501` to access the Streamlit frontend.

2. Upload JPG or PNG images using the file uploader widget.

3. Click the "Convert to PDF" button to convert the uploaded images to a PDF.

4. Download the generated PDF using the provided download button.

## Project Structure

- [app.py](http://_vscodecontentref_/0): Streamlit frontend application.
- [converter.py](http://_vscodecontentref_/1): FastAPI backend application for handling file uploads and conversions.
- [Dockerfile](http://_vscodecontentref_/2): Dockerfile for building the application container.
- [docker-compose.yml](http://_vscodecontentref_/3): Docker Compose file for setting up the application services.

## API Endpoints

- `POST /upload/`: Accepts multiple image files, saves them, and converts them into a PDF.

## Example

1. Upload images using the Streamlit interface:

    ![Upload Images](images/upload.png)

2. Click "Convert to PDF":

    ![Convert to PDF](images/convert.png)

3. Download the generated PDF:

    ![Download PDF](images/download.png)

## Author

- Marina CHAU

## License

This project is licensed under the MIT License.