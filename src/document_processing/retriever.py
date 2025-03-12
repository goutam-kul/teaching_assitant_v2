from langchain_chroma import Chroma
from src.database.chroma_client import ChromaClient
from src.document_processing.ollama_embedding import OllamaEmbeddingFunction
from loguru import logger


class DocumentRetriever:
    def __init__(self):
        self.client = ChromaClient()
        self.collection = None
        self.embedding_function = None
        self.collection_name = None

    def get_chunks(self, query: str, collection_name: str, k: int = 5):
        """Get the most relevant chunks for a query."""
        if not self.collection or collection_name != self.collection_name:
            self.embedding_function = OllamaEmbeddingFunction()
            self.collection_name = collection_name
            self.collection = self.client.get_or_create_collection(collection_name, embedding_function=self.embedding_function)

        query_embedding = self.embedding_function.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        logger.info(f"Retrieved {len(results['documents'][0])} chunks")
        return results


# Example usage
if __name__ == "__main__":
    collection_name = "statistics_book"
    retriever = DocumentRetriever()
    question = "What does the document say about the topic mean deviation?"
    chunks = retriever.get_chunks(query=question, collection_name=collection_name)
    print("Retrieved chunks:")
    for i, (doc, metadata, distance) in enumerate(zip(chunks['documents'][0], chunks['metadatas'][0], chunks['distances'][0])):
        print(f"\nChunk {i+1} (Distance: {distance:.4f}):")
        print(f"Source: {metadata['source']}")
        print(f"Content: {doc[:200]}...")  # Print first 200 chars of each chunk

    from src.llm.handler import LLMHandler
    llm = LLMHandler()
    response = llm.generate_explanation(question, chunks['documents'][0])
    print(response)