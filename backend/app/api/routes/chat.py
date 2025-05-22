from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

from core.chat_chain import get_chat_chain

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    domain: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[Dict[str, Any]]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process a chat request and return a response using LangChain.
    """
    try:
        # Get the user's message (last message in the list)
        if not request.messages or request.messages[-1].role != "user":
            raise HTTPException(status_code=400, detail="Last message must be from user")
        
        user_message = request.messages[-1].content
        
        # Get chat history (all previous messages)
        chat_history = []
        for i in range(0, len(request.messages) - 1, 2):
            if i + 1 < len(request.messages) - 1:
                if request.messages[i].role == "user" and request.messages[i+1].role == "assistant":
                    chat_history.append((request.messages[i].content, request.messages[i+1].content))
        
        # Get chat chain
        chat_chain = get_chat_chain()
        
        # Get response from chain
        result = chat_chain({"question": user_message, "chat_history": chat_history})
        
        # Return response
        return ChatResponse(
            response=result.get("answer", "I don't know how to respond to that."),
            sources=result.get("source_documents", [])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 