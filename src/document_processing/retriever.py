from langchain_chroma import Chroma
from src.database.chroma_client import ChromaClient
from src.document_processing.ollama_embedding import OllamaEmbeddingFunction
from loguru import logger
class DocumentRetriever:
    def __init__(self, collection_name: str, embedding_function: OllamaEmbeddingFunction):
        self.collection_name = collection_name
        self.embedding_function = embedding_function
        self.client = ChromaClient()
        self.collection = self.client.get_or_create_collection(collection_name, embedding_function=embedding_function)

    def get_chunks(self, query: str, k: int = 5):
        """Get the most relevant chunks for a query."""
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
    retriever = DocumentRetriever(collection_name=collection_name, embedding_function=OllamaEmbeddingFunction())
    question = "What does the document say about the topic mean deviation?"
    chunks = retriever.get_chunks(query=question)
    print("Retrieved chunks:")
    for i, (doc, metadata, distance) in enumerate(zip(chunks['documents'][0], chunks['metadatas'][0], chunks['distances'][0])):
        print(f"\nChunk {i+1} (Distance: {distance:.4f}):")
        print(f"Source: {metadata['source']}")
        print(f"Content: {doc[:200]}...")  # Print first 200 chars of each chunk

    from src.llm.handler import LLMHandler
    llm = LLMHandler()
    response = llm.generate_explanation(question, chunks['documents'][0])
    print(response)