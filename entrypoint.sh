#!/bin/bash
set -e

# شغل ollama على 0.0.0.0 عشان Render يوصل له
OLLAMA_HOST=0.0.0.0 ollama serve &


sleep 5


exec "$@"

