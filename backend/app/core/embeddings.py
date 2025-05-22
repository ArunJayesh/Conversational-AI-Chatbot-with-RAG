import os
import uuid
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader
)
from langchain_community.vectorstores import Chroma

# Load environment variables
load_dotenv()

# Set up global variables
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
COLLECTION_NAME = "arun_jayesh_assistant"

# File type to loader mapping
LOADER_MAPPING = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".html": UnstructuredHTMLLoader,
    ".htm": UnstructuredHTMLLoader,
}

def get_vectorstore():
    """
    Get or create a Chroma vector store.
    """
    # Create embeddings using HuggingFace model
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Create or get persistent vector store
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )
    
    return vectorstore

def get_document_loader(file_path):
    """
    Get the appropriate document loader based on file extension.
    """
    # Get file extension
    ext = os.path.splitext(file_path)[1].lower()
    
    # Get loader class
    loader_class = LOADER_MAPPING.get(ext)
    
    if not loader_class:
        raise ValueError(f"Unsupported file type: {ext}")
    
    # Return loader instance
    return loader_class(file_path)

def embed_document(text=None, file_path=None, metadata=None):
    """
    Embed a document into the vector store.
    Either text or file_path must be provided.
    """
    # Initialize metadata if not provided
    if metadata is None:
        metadata = {}
    
    # Generate document ID
    doc_id = str(uuid.uuid4())
    metadata["doc_id"] = doc_id
    
    # Get documents
    documents = []
    
    if text:
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Split text into chunks
        chunks = text_splitter.split_text(text)
        
        # Create documents
        documents = [{"page_content": chunk, "metadata": metadata} for chunk in chunks]
    
    elif file_path:
        # Get loader
        loader = get_document_loader(file_path)
        
        # Load documents
        loaded_docs = loader.load()
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Split documents
        documents = text_splitter.split_documents(loaded_docs)
        
        # Add metadata to each document
        for doc in documents:
            doc.metadata.update(metadata)
    
    else:
        raise ValueError("Either text or file_path must be provided")
    
    # Get vector store
    vectorstore = get_vectorstore()
    
    # Add documents to vector store
    vectorstore.add_documents(documents)
    
    # Persist vector store
    if hasattr(vectorstore, "_persist"):
        vectorstore._persist()
    
    return doc_id 