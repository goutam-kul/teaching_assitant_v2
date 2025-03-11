from typing import List, Dict, Any
from dotenv import load_dotenv
from llama_cloud_services import LlamaParse
from llama_index.core import SimpleDirectoryReader
import os
import logging
import re
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFParser:
    """Simple PDF parser using LlamaParse."""

    def __init__(self, result_type: str = "text"):
        """Initialize the PDF parser."""
        self.llama_parse = LlamaParse(
            result_type=result_type,
            api_key=os.getenv("LLAMA_CLOUD_API_KEY"),   
        )
        self.file_extractor = {".pdf": self.llama_parse}
        
    def clean_text(self, text: str) -> str:
        """Clean the text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading and trailing whitespace
        text = text.strip()
        return text
    
    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """Extract text from a PDF file."""
        logger.info(f"Extracting text from {file_path}")
        try:
            # Parse document
            documents = SimpleDirectoryReader(
                input_files=[file_path],
                recursive=False,
                file_extractor=self.file_extractor,
            ).load_data()
            logger.info(f"Extracted {len(documents)} documents from {file_path}")
            
            if not documents:
                logger.warning(f"No documents extracted from {file_path}")
                return {
                    "status": "error",
                    "message": "No documents extracted from the file",
                    "text": ""
                }
            
            # Clean the text
            clean_text = [self.clean_text(doc.text) for doc in documents]
            clean_text = "\n".join(clean_text)
            return clean_text
        
        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return {
                "status": "error",
                "message": f"Failed to extract text from {file_path}: {e}",
                "text": ""
            }
        
# Example usage
if __name__ == "__main__":
    parser = PDFParser()
    file_path = "data/test.pdf"
    text = parser.extract_text(file_path)
    print(text)