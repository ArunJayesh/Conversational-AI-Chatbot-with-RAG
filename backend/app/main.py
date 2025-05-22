from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Conversational AI Chatbot with RAG",
    description="A domain-specific assistant chatbot using LangChain and ChromaDB",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from api.routes import chat, embed, projects

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(embed.router, prefix="/api", tags=["embed"])
app.include_router(projects.router, prefix="/api", tags=["projects"])

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {"message": "Conversational AI Chatbot API is running!"}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True) 