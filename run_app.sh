#!/bin/bash

# Print a message
echo "Starting RAG Chatbot Application..."

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/version &>/dev/null; then
  echo "Warning: Ollama doesn't seem to be running. Please start it with 'ollama serve'"
  echo "You can install Ollama from https://ollama.ai if not already installed"
  echo "-----------------------------------------------------"
fi

# Start the backend in the background
echo "Starting backend server..."
cd backend
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ../../

# Start the frontend in the background
echo "Starting frontend server..."
cd frontend
npm install
npm start &
FRONTEND_PID=$!
cd ..

# Function to handle script termination
cleanup() {
  echo "Shutting down servers..."
  kill $BACKEND_PID
  kill $FRONTEND_PID
  exit 0
}

# Set up trap to handle Ctrl+C
trap cleanup SIGINT

echo "-----------------------------------------------------"
echo "RAG Chatbot is running!"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "-----------------------------------------------------"
echo "Press Ctrl+C to stop all servers"

# Keep the script running
wait 