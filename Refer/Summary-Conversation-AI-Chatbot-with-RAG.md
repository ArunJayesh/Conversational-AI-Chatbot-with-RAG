# Conversational AI Chatbot with RAG - Project Summary

## Project Overview
A conversational AI chatbot that provides information about Arun Jayesh's projects. The application uses Retrieval Augmented Generation (RAG) to enhance responses with relevant information from a knowledge base about Arun's projects.

## Architecture

### Frontend
- **Framework**: React with Material UI
- **Design**: Custom UI based on Figma designs with dark theme
- **Features**: Real-time chat interface with typing indicators, message history, and styled message bubbles

### Backend
- **Framework**: FastAPI (Python)
- **Features**: RESTful API endpoints for chat interactions

### Models and Tools

#### Language Model
- **Model**: Mistral (via Ollama)
- **Hosting**: Local deployment through Ollama (port 11434)
- **Purpose**: Text generation and conversation management

#### Vector Database
- **Database**: ChromaDB
- **Embeddings**: HuggingFace embeddings
- **Purpose**: Storage and retrieval of vector representations of documents

#### RAG Implementation
- **Library**: LangChain
- **Components**:
  - ConversationalRetrievalChain for combining context and conversation
  - ConversationBufferMemory for maintaining chat history
  - Custom prompt templates to guide model responses

## Implementation Steps

### 1. Backend Setup
- Created FastAPI application structure with appropriate routes
- Implemented LangChain integration with Ollama for local LLM access
- Set up document ingestion pipeline to convert documents about Arun's projects into vector embeddings
- Created a chat chain combining retrieval capabilities with conversation history
- Implemented proper error handling and API response formatting

### 2. Frontend Development
- Created React application with Material UI components
- Implemented basic chat interface with input field and message display
- Added API integration to communicate with backend
- Styled components according to design specifications:
  - Black background with green (#49E883) accents
  - Custom message bubbles with different shapes for user and assistant
  - Three-dot loading animation during response generation

### 3. UI Refinements
- Added proper user identification labels ("USER" and "AJ'S HELPER") above messages
- Modified header styling with rounded corners at the bottom
- Updated welcome message to specify information about "Arun Jayesh's projects"
- Implemented responsive design elements
- Added message history scrolling with automatic scroll to newest messages

### 4. Final Touchups
- Fixed send button issues by embedding SVG icons directly in the React component
- Added proper loading indicators
- Ensured proper border styling and coloring throughout the application
- Fixed minor UI inconsistencies

## Challenges Faced and Solutions

### 1. API Connection Issues
- **Problem**: Initial challenges connecting frontend to backend API
- **Solution**: Configured proper CORS settings and ensured API routes matched frontend expectations

### 2. UI Styling Challenges
- **Problem**: Difficulty achieving exact Figma design, especially with message bubbles and rounded corners
- **Solution**: Used nested Box components to properly implement the rounded corner design, especially for the header

### 3. Asset Loading Issues
- **Problem**: SVG icons not loading correctly from the assets folder
- **Solution**: Embedded SVG components directly in the React code instead of loading them as external files

### 4. Model Output Formatting
- **Problem**: Raw model outputs sometimes lacked proper formatting
- **Solution**: Used ReactMarkdown to render model responses with proper formatting

### 5. Port Conflicts
- **Problem**: Port conflicts when running multiple services (Ollama, backend, frontend)
- **Solution**: Configured different ports for each service and ensured proper routing

## LangChain Configuration Details

### Chat Chain Setup
```python
def get_chat_chain(temperature=0.7, model_name="mistral"):
    # Initialize LLM with Ollama using mistral model
    llm = OllamaLLM(
        model=model_name,
        temperature=temperature,
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )
    
    # Get vector store
    vectorstore = get_vectorstore()
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    
    # Create memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    # Create prompt
    prompt = PromptTemplate(
        template=DEFAULT_TEMPLATE,
        input_variables=["context", "chat_history", "question"]
    )
    
    # Create chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        verbose=True,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )
    
    return qa_chain
```

### Prompt Template
```
You are a helpful AI assistant that provides information about Arun Jayesh and his projects.
The person using you is NOT Arun Jayesh - they are someone asking about Arun and his work.
Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
Don't try to make up an answer. Always maintain a helpful, friendly tone.

Context: {context}

Chat History: {chat_history}

Question: {question}

Answer:
```

## Running the Application

### Backend
```bash
cd backend && source venv/bin/activate && cd app && python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend && npm start
```

### Ollama
```bash
ollama serve
```

## Future Improvements

1. Update LangChain dependencies to address deprecation warnings
2. Enhance error handling with more user-friendly error messages
3. Add authentication for secure access
4. Implement streaming responses for better user experience
5. Add additional document ingestion methods for expanding the knowledge base
6. Improve the prompt template for more accurate and helpful responses
7. Add user feedback mechanisms to improve system responses over time 