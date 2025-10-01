#!/bin/bash

ollama serve &

sleep 5

ollama pull gemma3:4b

sleep 10

exec "$@"
