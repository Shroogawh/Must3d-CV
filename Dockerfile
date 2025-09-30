# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PyMuPDF, pytesseract, and Pillow
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-ara \
    libpng-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Set environment variable for Ollama model
ENV OLLAMA_MODEL=gemma3:7b

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
