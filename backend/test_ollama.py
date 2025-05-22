import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
import time

# Load environment variables
load_dotenv()

def test_ollama_llm():
    """Test the Ollama LLM integration."""
    print("Testing Ollama LLM integration...")
    
    # Initialize Ollama LLM
    llm = OllamaLLM(
        model="mistral",
        temperature=0.7,
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )
    
    # Test with a simple prompt
    prompt = "What is Retrieval Augmented Generation (RAG)?"
    print(f"Sending prompt: {prompt}")
    
    # Measure response time
    start_time = time.time()
    response = llm.invoke(prompt)
    end_time = time.time()
    
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Response: {response}")
    print("Ollama LLM test completed.\n")

def test_huggingface_embeddings():
    """Test the HuggingFace embeddings."""
    print("Testing HuggingFace embeddings...")
    
    # Initialize HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Test with a simple text
    text = "Retrieval Augmented Generation (RAG) is a technique that combines retrieval-based and generation-based approaches for natural language processing tasks."
    print(f"Generating embeddings for: {text[:50]}...")
    
    # Measure embedding time
    start_time = time.time()
    embedding = embeddings.embed_query(text)
    end_time = time.time()
    
    print(f"Embedding time: {end_time - start_time:.2f} seconds")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print("HuggingFace embeddings test completed.")

if __name__ == "__main__":
    test_ollama_llm()
    test_huggingface_embeddings() 