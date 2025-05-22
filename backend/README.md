# RAG Chatbot Backend

This is the backend for the Conversational AI Chatbot with RAG (Retrieval Augmented Generation) project. The backend is built with FastAPI, LangChain, and ChromaDB.

## Prerequisites

- Python 3.10+
- Ollama installed with mistral model
- 5GB+ disk space for models

## Setup and Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the backend directory:
   ```
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   HOST=localhost
   PORT=8000
   OLLAMA_HOST=http://localhost:11434
   ```

4. Make sure Ollama is running:
   ```
   ollama serve
   ```

5. Check if the mistral model is installed:
   ```
   ollama list
   ```

   If not, pull the mistral model:
   ```
   ollama pull mistral
   ```

## Running the Backend

1. Start the FastAPI server:
   ```
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Test the Ollama integration:
   ```
   python test_ollama.py
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

## Technologies Used

- FastAPI for the web framework
- LangChain for orchestrating the LLM and embedding models
- Ollama with mistral model for LLM processing
- HuggingFace for embeddings
- ChromaDB for vector storage 
 