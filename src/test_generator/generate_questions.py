from typing import List, Dict, Any
from src.llm.handler import LLMHandler
from loguru import logger
import json


class QuestionGenerator:

    def __init__(self):
        self.llm_handler = LLMHandler()

    def generate_question_variants(self, original_question: str) -> str:
        """Generate variants for the original question"""
        variants = self.llm_handler.generate_query_variants(question=original_question)
        return variants 
    
    def generate_question_from_topic(self, topic: str, num_questions: int) -> List[str]:
        """Generate questions from a given topic"""
        # Generate questions from the topic
        questions = self.llm_handler.generat_questions_from_topic(topic=topic, num_questions=num_questions)
        # Parse the output from LLM
        questions = json.loads(questions)
        return questions["questions"]
    
    def evaluate_test(self, questions: List[str], answers: List[str]) -> Dict[str, Any]:
        """Evaluate the test"""
        question_answer_pair = {
            f"question{i + 1}": {"question": question, "answer":answer} for i, (question, answer) in enumerate(zip(questions, answers))
        }
        evaluation = self.llm_handler.evaluate_test(question_answer_pair=question_answer_pair)
        return evaluation

if __name__ == "__main__":
    question_generator = QuestionGenerator()
    questions = question_generator.generate_question_from_topic(topic="Statistics")
    print(questions)



