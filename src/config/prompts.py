TEMPLATE = """You are a teaching assistant tasked with answerting questions based on the provided context ONLY.
Generate a meaningful explanation provided by the context

Question: {question}

Relevant Context:
{context}

INSTRUCTIONS:
- Answer the question based on the proivded context ONLY.
- Summarize the context to create a meaningful explanation.
- If the context does not contain the answer, say "I couldn't find any relevant information about the topic in the provided context."
- If the question is not related to the context, say "I couldn't find any relevant information about the topic in the provided context."
- Be concise and to the point.
- Do not make up or add information not provided in the context.

Your Response:
"""

IMAGE_CAPTION_TEMPLATE = """Based on the provided context, generate a caption for the image.

Context: {image_context}

INSTRUCTIONS:
- Generate a caption for the image.
- Be concise and to the point.
- Do not make up or add information not provided in the image.
"""

QUERY_VARIANT_PROMPT = """You are a teaching assistant, your job is to generate variants for the original question asked. 
RETURN THE VARIANTS IN A LIST OF STRINGS ONLY.

Original Question: {question}

INSTRUCTIONS:
- Generate 5 different query variants for the original question.
- The variants should be different from the original question.
- The variants MUST be related to the original question.
- The variants should be in the same language as the original question.

"""

QUESTION_FROM_TOPIC_PROMPT = """You are a teaching assistant, you job is to generate questions for the given topic.
RETURN the questions as a valid JSON response ONLY.

INSTRUCTIONS:
- Generate {num_questions} questions on the provided topic.
- The questions MUST be related to the provided topic.
- The question MUST not be duplicates.
- The questions should test the understanding of the topic.
- The questions should test the application of the topic.
- The questions should test the analysis of the topic.
- The questions should test the synthesis of the topic.
- The questions should test the evaluation of the topic.
- The questions should test the creation of the topic.
- The questions should test the application of the topic.

OUTPUT FORMAT:
{{
    "questions": [
        "question1",
        "question2",
        "question3",
        "question4",
        "question5"
    ]
}}
Topic: {topic}
"""

EVALUATE_TEST_PROMPT = """You are a teaching assistant, your job is to evaluate the answer written by the user for the respective question.

Question answer pairs to evaluate:
{question_answer_pair}

INSTRUCTIONS:
- Evaluate the answers provided by the student.
- Score the answer between 0 and 5.
- 0 means the answer is incorrect.
- 1 means the answer is partially correct.
- 2 means the answer is correct.
- 3 means the answer is correct and the student has applied the knowledge.
- 4 means the answer is correct and the student has applied the knowledge and the student has analyzed the topic.
- 5 means the answer is correct and the student has applied the knowledge and the student has analyzed the topic and the student has synthesized the topic.

You must return a JSON object where each key matches the original question number and contains a score and feedback.
For example, if the input has question1 and question2, your response should look exactly like this:
{{
    "question1": {{
        "score": 3,
        "feedback": "Detailed feedback for question 1"
    }},
    "question2": {{
        "score": 4,
        "feedback": "Detailed feedback for question 2"
    }}
}}"""
