from typing import List, Dict, Any
from src.database.chroma_client import ChromaClient
from src.document_processing.pdf_extractor import PDFParser
from src.document_processing.ollama_embedding import OllamaEmbeddingFunction
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentPopulator:
    """Class to populate the database with documents."""

    def __init__(self, collection_name: str = "documents"):
        """Initialize the DocumentPopulator"""
        self.chroma_client = ChromaClient()
        self.collection_name = collection_name
        self.pdf_parser = PDFParser(result_type="text")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
            # separators=["\n\n", "\n", ". ", ". ", " ", ""]
        )
        self.ollama_ef = OllamaEmbeddingFunction()


    def process_file_and_add_to_db(
        self, collection_name: str, file_path: str, reset_collection: bool = False
    ):
        """Process a file and add it to the database."""
        try:
            logger.info(f"Processing file {file_path}")
            if reset_collection:
                try:
                    self.chroma_client.delete_collection(collection_name)
                    logger.info(f"Collection '{collection_name}' deleted successfully.")
                except Exception as e:
                    logger.error(f"Error deleting collection '{collection_name}': {e}")

            # Parse pdf into documents
            raw_text = self.pdf_parser.extract_text(file_path=file_path)
            logger.info(f"Successfully extracted text from {file_path}")

            # Split the text into chunks
            chunks = self.text_splitter.create_documents([raw_text])
            logger.info(f"Successfully split text into {len(chunks)} chunks")

            logger.info(f"Embedding {len(chunks)} chunks")
            # Embed the chunks
            chunk_embeddings = self.ollama_ef.embed_documents(
                [chunk.page_content for chunk in chunks]
            )
            logger.info(f"Successfully embedded {len(chunks)} chunks")

            # Add the chunks to the database
            collection = self.chroma_client.get_or_create_collection(collection_name)

            # Prepare the data for the database
            texts = [chunk.page_content for chunk in chunks]
            metadata = [{"source": file_path, "chunk_id": i} for i, _ in enumerate(chunks)]
            ids = [f"Chunk_{i}_{Path(file_path).stem}" for i, _ in enumerate(chunks)]

            logger.info(f"Adding {len(chunks)} chunks to the database")
            # Add the data to the database
            collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadata,
                embeddings=chunk_embeddings,
            )
            logger.info(f"Successfully added {len(chunks)} chunks to the database")
            
            return {
                "status": "success",
                "message": f"Successfully processed file {file_path}",
                "file_path": file_path,
                "collection_name": collection_name,
                "num_chunks": len(chunks),
            }

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return {
                "status": "error",
                "message": f"Error processing file {file_path}: {e}",
                "file_path": file_path,
                "collection_name": collection_name,
                "num_chunks": 0,
            }
            

# Example usage
if __name__ == "__main__":
    populator = DocumentPopulator()
    result = populator.process_file_and_add_to_db(
        collection_name='test_collection',
        file_path='data/test.pdf',
        reset_collection=True
    )
    from src.document_processing.retriever import DocumentRetriever
    retriever = DocumentRetriever(collection_name="test_collection", embedding_function=populator.ollama_ef)
    print(retriever.get_chunks(query="What is the main topic of the document?"))