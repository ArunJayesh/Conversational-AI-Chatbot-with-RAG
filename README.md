# Conversational AI Chatbot with RAG

A domain-specific assistant chatbot using LangChain, ChromaDB, Ollama, and FastAPI with a React frontend.

## Features

- **Local AI Processing**: Uses Ollama with the mistral model for local LLM inference
- **Free Vector Embeddings**: HuggingFace Embeddings with all-MiniLM-L6-v2 model
- **Document Processing**: Support for PDF, DOCX, TXT, HTML files
- **Vector Database**: ChromaDB for similarity search
- **Modern UI**: React-based frontend with Material UI
- **Temporary Public Access**: Option to expose the API using ngrok

## Prerequisites

- Python 3.10+
- Node.js 14+ and npm
- Ollama installed with mistral model
- 5GB+ disk space for models

## Installation

1. **Install Ollama**

   Download and install Ollama from [https://ollama.com/download](https://ollama.com/download)

2. **Pull the mistral model**

   ```bash
   ollama pull mistral
   ```

3. **Clone this repository**

   ```bash
   git clone <repository-url>
   cd Conversational-AI-Chatbot-with-RAG
   ```

4. **Set up the backend**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Configure environment variables**

   Create a `.env` file in the backend directory:

   ```
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   HOST=localhost
   PORT=8000
   OLLAMA_HOST=http://localhost:11434
   ```

6. **Set up the frontend**

   ```bash
   cd frontend
   npm install
   ```

## Running the Application

### Quick Start (Recommended)

Use the provided script to start both frontend and backend:

```bash
./run_app.sh
```

This will:
- Check if Ollama is running
- Start the backend server
- Start the frontend development server
- Open the application in your browser

### Manual Start

1. **Run the backend server**

   ```bash
   cd backend/app
   python -m uvicorn main:app --host localhost --port 8000
   ```

2. **Run the frontend server**

   ```bash
   cd frontend
   npm start
   ```

3. **Test the Ollama integration**

   ```bash
   cd backend
   python test_ollama.py
   ```

4. **Run with ngrok for temporary public access**

   First, sign up for ngrok and get your authtoken from [https://dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)

   Set the authtoken in your environment:
   ```bash
   export NGROK_AUTHTOKEN=your_authtoken_here
   ```

   Then run:
   ```bash
   cd backend
   python run_with_ngrok.py
   ```

## API Endpoints

- **Chat API**
  - `POST /api/chat`: Process chat messages with RAG

- **Embed API**
  - `POST /api/embed/text`: Embed text into the vector store
  - `POST /api/embed/file`: Upload and embed documents (PDF, DOCX, TXT, HTML)
  - `GET /api/embed/status`: Get vector store status

- **Projects API**
  - `POST /api/projects`: Create a new project
  - `GET /api/projects`: List all projects
  - `GET /api/projects/{id}`: Get a specific project
  - `PUT /api/projects/{id}`: Update a project
  - `DELETE /api/projects/{id}`: Delete a project

## Architecture

The system uses a Retrieval Augmented Generation (RAG) architecture:

1. **Vector Store**: ChromaDB stores document embeddings
2. **Embeddings**: HuggingFace Embeddings (all-MiniLM-L6-v2)
3. **LLM**: Ollama with mistral model for conversational responses
4. **API**: FastAPI for handling requests
5. **Frontend**: React with Material UI
6. **Temporary Deployment**: ngrok for public access

## License

This project is licensed under the MIT License - see the LICENSE file for details. 