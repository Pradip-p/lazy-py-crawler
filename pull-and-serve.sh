#!/bin/sh
# pull-and-serve.sh

# Start Ollama server in the background
ollama serve &

# Wait a few seconds for the server to initialize
sleep 5

# Pull the model if missing
if ! ollama list | grep -q "qwen2.5:0.5b"; then
  echo "Pulling model qwen2.5:0.5b..."
  ollama pull qwen2.5:0.5b
else
  echo "Model qwen2.5:0.5b already present."
fi

# Bring the server to the foreground so container stays alive
fg %1
