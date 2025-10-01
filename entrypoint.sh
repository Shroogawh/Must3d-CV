#!/bin/bash
export OLLAMA_HOST=0.0.0.0:11434  
ollama serve &
sleep 10  
ollama pull gemma3:4b
sleep 60 
exec "$@"
