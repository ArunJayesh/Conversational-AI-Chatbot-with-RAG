import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

from core.embeddings import get_vectorstore

# Load environment variables
load_dotenv()

# Default prompt template
DEFAULT_TEMPLATE = """
You are a helpful AI assistant that provides information about Arun Jayesh and his projects.
The person using you is NOT Arun Jayesh - they are someone asking about Arun and his work.
Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know.
Don't try to make up an answer. Always maintain a helpful, friendly tone.

Context: {context}

Chat History: {chat_history}

Question: {question}

Answer:
"""

def get_chat_chain(temperature=0.7, model_name="mistral"):
    """
    Create and return a conversational retrieval chain using Ollama with mistral model.
    """
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