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
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN curl -fsSL https://ollama.com/install.sh | sh


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


COPY . .
COPY .env .env


EXPOSE 8000
EXPOSE 11434


ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
