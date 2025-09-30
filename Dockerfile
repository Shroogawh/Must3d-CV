FROM python:3.10-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-ara \
    libpng-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

# تثبيت Ollama
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*


COPY . .
COPY .env .env


EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
