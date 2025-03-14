from typing import List, Dict, Any
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config.prompts import TEMPLATE, QUERY_VARIANT_PROMPT, QUESTION_FROM_TOPIC_PROMPT, EVALUATE_TEST_PROMPT
from loguru import logger
from src.config.settings import get_settings
from io import BytesIO
from PIL import Image
import base64
import json

settings = get_settings()


class LLMHandler:
    """Base class for LLM handlers"""
    def __init__(self):
        self.text_model = OllamaLLM(model=settings.text_model)
        self.image_model = OllamaLLM(model=settings.image_model)
        self.text_base_template = ChatPromptTemplate.from_template(TEMPLATE)
        self.parser = StrOutputParser()
        self.text_chain = self.text_base_template | self.text_model | self.parser


    def convert_image_to_base64(self, image_path: str) -> str:
        """Convert an image to base64 format."""
        pil_image = Image.open(image_path)
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str
    
    def generate_image_caption(self, image_path: str, prompt: str) -> str:
        """Generate a caption for an image."""
        img_str = self.convert_image_to_base64(image_path=image_path)
        llm_with_image_context = self.image_model.bind(images=[img_str])
        return llm_with_image_context.invoke(prompt)

    def generate_explanation(self, question: str, context: List[str]) -> str:
        """Generate an explanation for a question based on the provided context."""
        logger.info(f"Generating explanation for question: {question}")
        return self.text_chain.invoke({"question": question, "context": context})
    
    def generate_query_variants(self, question: str) -> List[str]:
        """Generate multiple query variants for a given question."""
        logger.info(f"Generating query variants for question: {question}")
        prompt = QUERY_VARIANT_PROMPT.format(question=question)
        return self.text_model.invoke(prompt)
    
    def generat_questions_from_topic(self, topic: str, num_questions: int) -> Dict[str, Any]:
        """Generate questions from a given topic."""
        logger.info(f"Generating question for topic: {topic}")
        prompt = QUESTION_FROM_TOPIC_PROMPT.format(topic=topic, num_questions=num_questions)
        return self.text_model.invoke(prompt)
    
    def evaluate_test(self, question_answer_pair: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the test answers."""
        try:
            logger.info("Evaluating the answers")
            # Format the question_answer_pair as a string for better prompt formatting
            formatted_pairs = json.dumps(question_answer_pair, indent=2)
            logger.info(f"Formatted question answer pairs: {formatted_pairs}")
            
            # Create and format the prompt
            prompt = EVALUATE_TEST_PROMPT.format(question_answer_pair=formatted_pairs)
            logger.info(f"Generated prompt: {prompt}")
            
            # Get response from LLM
            response = self.text_model.invoke(prompt)
            logger.info(f"Raw LLM response: {response}")
            
            # Try to parse the response as JSON
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                    logger.info(f"Parsed response: {response}")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse LLM response as JSON: {response}")
                    logger.error(f"JSON decode error: {str(e)}")
                    return {"error": "Failed to parse evaluation response"}
            
            return response
        except Exception as e:
            logger.error(f"Error in evaluate_test: {str(e)}")
            return {"error": f"Evaluation failed: {str(e)}"}


if __name__ == "__main__":
    llm = LLMHandler()
    # print(llm.generate_explanation("What is the capital of France?", ["France is a country in Europe.", "Paris is the capital of France."]))
    # print(llm.generate_image_caption("data/images/test_image.png", "Please describe this image in detail."))
    # response = llm.generate_query_variants("What is mean, median and mode?")
    # print(type(response))
    # print(response)
    response = llm.generat_questions_from_topic("Statistics")
    print(type(response))
    print(response)