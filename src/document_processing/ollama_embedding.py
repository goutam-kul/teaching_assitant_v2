from langchain_ollama import OllamaEmbeddings
from chromadb.utils import embedding_functions

class OllamaEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model: str = "nomic-embed-text:latest"):
        self.model = model
        self.embeddings = OllamaEmbeddings(model=model)

    def embed_query(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.embeddings.embed_documents(texts)

    
if __name__ == "__main__":
    ollama_ef = OllamaEmbeddingFunction()
    print(len(ollama_ef.embed_query("Hello, world!")))
    print(ollama_ef.embed_documents(["Hello, world!", "Hello, world!"]))