FROM python:3.11-slim


RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --default-timeout=1000
COPY . .

# Pull a small model (gemma3:4b is large, try tinyllama for testing)
RUN ollama pull tinyllama

EXPOSE 8000
EXPOSE 11434


CMD ollama serve & sleep 10 && uvicorn main:app --host 0.0.0.0 --port 8000
