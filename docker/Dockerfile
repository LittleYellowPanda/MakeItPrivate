# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Install UV package manager
RUN pip install uv

# Copy essential files from the project root
COPY requirements.txt pyproject.toml app.py /app/
COPY src /app/src/

# Install dependencies using UV
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install --no-cache-dir -r requirements.txt

# Expose FastAPI and Streamlit ports
EXPOSE 8000 8501

# Start FastAPI and Streamlit apps
CMD ["sh", "-c", ". .venv/bin/activate && uvicorn src.fastapi_app:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
