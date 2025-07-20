FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y build-essential

# Set working directory
# WORKDIR /simteam

# Copy entire project (preserving layout)
COPY . .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Entrypoint: run both FastAPI and Streamlit via run_app.py
CMD ["python", "run_app.py"]
