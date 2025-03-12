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
- Generate 10 questions on the provided topic.
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
