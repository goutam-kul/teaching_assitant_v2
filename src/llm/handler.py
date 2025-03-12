from typing import List, Dict, Any
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config.settings import TEMPLATE
from loguru import logger


class LLMHandler:
    """Base class for LLM handlers"""
    def __init__(self, model_name: str = "mistral:latest"):
        self.model = OllamaLLM(model=model_name)
        self.base_template = ChatPromptTemplate.from_template(TEMPLATE)
        self.parser = StrOutputParser()
        self.chain = self.base_template | self.model | self.parser
    
    def generate_explanation(self, question: str, context: List[str]) -> str:
        """Generate an explanation for a question based on the provided context."""
        logger.info(f"Generating explanation for question: {question}")
        return self.chain.invoke({"question": question, "context": context})


if __name__ == "__main__":
    llm = LLMHandler()
    print(llm.generate_explanation("What is the capital of France?", ["France is a country in Europe.", "Paris is the capital of France."]))