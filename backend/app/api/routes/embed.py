from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile

from core.embeddings import embed_document, get_vectorstore

router = APIRouter()

class EmbedTextRequest(BaseModel):
    text: str
    metadata: Optional[dict] = None

class EmbedResponse(BaseModel):
    success: bool
    message: str
    document_id: Optional[str] = None

@router.post("/embed/text", response_model=EmbedResponse)
async def embed_text(request: EmbedTextRequest):
    """
    Embed a text document into the vector store.
    """
    try:
        doc_id = embed_document(text=request.text, metadata=request.metadata)
        return EmbedResponse(
            success=True,
            message="Text embedded successfully",
            document_id=doc_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embed/file", response_model=EmbedResponse)
async def embed_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None)
):
    """
    Embed a file document into the vector store.
    """
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Process metadata
        meta = {}
        if metadata:
            import json
            meta = json.loads(metadata)
        
        # Add filename to metadata
        meta["filename"] = file.filename
        
        # Embed document
        doc_id = embed_document(file_path=temp_path, metadata=meta)
        
        # Clean up
        os.unlink(temp_path)
        
        return EmbedResponse(
            success=True,
            message=f"File {file.filename} embedded successfully",
            document_id=doc_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/embed/status")
async def embed_status():
    """
    Get status of the vector store.
    """
    try:
        # Get vector store
        vectorstore = get_vectorstore()
        
        # Get collection statistics
        collection = vectorstore._collection
        count = collection.count()
        
        return {
            "status": "operational",
            "document_count": count,
            "collection_name": collection.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 