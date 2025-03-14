from flask import Flask, render_template, request
from src.test_generator.generate_questions import QuestionGenerator
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate_test", methods=["POST"])
def generate_test():
    topic = request.form.get("topic")
    num_questions = request.form.get("num_questions")
    if not topic:
        return "Topic is required", 400
    
    question_generator = QuestionGenerator()
    questions = question_generator.generate_question_from_topic(topic=topic, num_questions=int(num_questions))
    # Add debug logging
    print("Generated questions for topic:", topic)
    print("Questions:", questions)
    return render_template("test.html", questions=questions, topic=topic)

@app.route("/submit_test", methods=["POST"])
def submit_test():
    # Get all questions and answers from the form
    questions = request.form.getlist('question[]')
    answers = request.form.getlist('answers[]')
    print("Questions received:", questions)
    print("Answers received:", answers)

    # Evaluate the test
    question_generator = QuestionGenerator()
    evaluation = question_generator.evaluate_test(questions=questions, answers=answers)
    
    # Add questions and answers to the evaluation data
    for i, (question, answer) in enumerate(zip(questions, answers), 1):
        question_key = f"question{i}"
        if question_key in evaluation:
            evaluation[question_key].update({
                "question": question,
                "answer": answer
            })
    
    print("Final evaluation data:", evaluation)
    return render_template("results.html", evaluation=evaluation)


if __name__ == '__main__':
    app.run(debug=True)