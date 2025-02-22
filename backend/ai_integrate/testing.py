from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from qnamodel import ChatBotSystem
import json
import os

app = Flask(__name__)
CORS(app)

# Load the knowledge base from a JSON file
KNOWLEDGE_BASE_FILE = "knowledge_base.json"
KNOWLEDGE_BASE = {}

def load_knowledge_base():
    """
    Load the knowledge base from a JSON file.
    """
    global KNOWLEDGE_BASE
    try:
        with open(KNOWLEDGE_BASE_FILE, "r") as file:
            KNOWLEDGE_BASE = json.load(file)
    except Exception as e:
        KNOWLEDGE_BASE = {}

# Load the knowledge base 
load_knowledge_base()

# Load the chatbot
chatbot = ChatBotSystem()


def preprocess_text(text: str) -> str:
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters (optional)
    text = re.sub(r'[^\w\s.,!?]', ' ', text)
    return text.strip()


def extract_relevant_context(text: str, question: str) -> str:
    # Extract the most relevant context from the text based on the question.
    # Split the text into sentences
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Find sentences that contain keywords from the question
    relevant_sentences = []
    question_keywords = set(question.lower().split())

    for sentence in sentences:
        sentence_keywords = set(sentence.lower().split())
        # Check if any keyword from the question is in the sentence
        if question_keywords.intersection(sentence_keywords):
            relevant_sentences.append(sentence)

    # Combine relevant sentences into a single context
    context = " ".join(relevant_sentences)
    return context if context else "No relevant context found for the question."


@app.route('/ask', methods=['POST'])
def ask_question():
    # Get question and uploaded file from the request
    question = request.form.get("question", "")
    file = request.files.get("file")

    if not question:
        return jsonify({"error": "A question is required."}), 400

    # If the user uploaded a file
    if file:
        # Preprocess the file
        file_text = file.read().decode("utf-8")
        file_text = preprocess_text(file_text)
        context = extract_relevant_context(file_text, question)
    else:
        # Use the knowledge base
        context = ""
        for key, value in KNOWLEDGE_BASE.items():
            if key in question.lower():
                context = value
                break

        if not context:
            context = "No relevant context found for the question."

    # Get the response from the chatbot
    response = chatbot.get_response(context, question)
    if response["success"]:
        return jsonify({"answer": response["response"]})
    else:
        return jsonify({"error": response["error"]}), 500
    
    

@app.route('/', methods=['GET'])
def home():
    return jsonify("[CONNECTED]")

if __name__ == "__main__":
    app.run(debug=True)