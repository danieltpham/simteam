# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run main process (FastAPI + Streamlit)
CMD ["python", "run_app.py"]
