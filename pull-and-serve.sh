#!/bin/sh
# pull-and-serve.sh
# Start Ollama server and pull required model

# # Start Ollama server in the background
# ollama serve &
# SERVER_PID=$!

# # Wait a few seconds for the server to initialize
# sleep 5

# # Pull the model if missing
# if ! ollama list | grep -q "qwen2.5:0.5b"; then
#   echo "Pulling model qwen2.5:0.5b..."
#   ollama pull qwen2.5:0.5b
# else
#   echo "Model qwen2.5:0.5b already present."
# fi

# # Keep the container alive by waiting for the background process
# wait $SERVER_PID


# Start Ollama server in the background
ollama serve &
SERVER_PID=$!

# Wait a few seconds for the server to initialize
sleep 5

# Pull the model if missing
if ! ollama list | grep -q "qwen2.5:32b"; then
  echo "Pulling model qwen2.5:32b..."
  ollama pull qwen2.5:32b
else
  echo "Model qwen2.5:32b already present."
fi

# Keep the container alive by waiting for the background process
wait $SERVER_PID
