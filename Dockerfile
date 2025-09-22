FROM python:3.12-slim

# Install system dependencies and Ollama
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --default-timeout=1000
COPY . .

EXPOSE 8000
EXPOSE 11434

# Start Ollama server, pull gemma3:4b, and run the app
CMD ollama serve & sleep 15 && ollama pull gemma3:4b && uvicorn main:app --host 0.0.0.0 --port 8000
