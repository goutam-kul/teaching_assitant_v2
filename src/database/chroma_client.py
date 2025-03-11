from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from src.document_processing.ollama_embedding import OllamaEmbeddingFunction

class ChromaClient:
    """Singleton class for ChromaDB client."""
    _instance = None

    def __new__(cls, persist_directory: str = "db"):
        """Ensure only one instance of ChromaClient exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False
                )
            ) if persist_directory else chromadb.Client()
        return cls._instance
    
    def __init__(self, embedding_function: OllamaEmbeddingFunction = None):
        self.ollama_ef = embedding_function or OllamaEmbeddingFunction()

    
    def create_collection(self, name: str):
        """Create a new collection if it doesn't exits."""
        if name not in self.client.list_collections():
            return self.client.create_collection(name)
        return self.client.get_collection(name)
    
    def delete_collection(self, name: str):
        """Delete an existing collection."""
        if name in self.client.list_collections():
            self.client.delete_collection(name)

    def list_collections(self):
        """List all collections."""
        return self.client.list_collections()
    
    def get_or_create_collection(self, name: str, embedding_function: OllamaEmbeddingFunction = None):
        """Get or create a collection."""
        return self.client.get_or_create_collection(name, embedding_function=embedding_function or self.ollama_ef)
    

