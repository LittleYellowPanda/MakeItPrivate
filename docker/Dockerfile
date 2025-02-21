FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Install UV package manager and dependencies
RUN pip install uv && \
    pip install streamlit

# Copy project files from the correct context
COPY src ./src   
COPY requirements.txt pyproject.toml app.py ./

# Install dependencies using UV
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install --no-cache-dir -r requirements.txt

# Ensure the shared directory exists
RUN mkdir -p /app/shared

# Expose FastAPI and Streamlit ports
EXPOSE 8000 8501

# Start FastAPI and Streamlit apps properly
CMD . .venv/bin/activate && uvicorn src.converter:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0

