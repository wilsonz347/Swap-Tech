from flask import Flask, jsonify, request
from flask_cors import CORS
from qnamodel import ChatBotSystem
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def find_most_similar_key(question, knowledge_base):
    # Find the most similar key and its value in the knowledge base 
    vectorizer = TfidfVectorizer(stop_words="english")
    
    # Combine both the keys and values for the knowledge base
    knowledge_base_combined = [key + " " + value for key, value in knowledge_base.items()]
    knowledge_base_keys = list(knowledge_base.keys())
    
    all_texts = [question] + knowledge_base_combined
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate cosine similarities 
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    # Find the highest similarity score
    most_similar_idx = cosine_sim.argmax()
    similarity_score = cosine_sim[0, most_similar_idx]
    
    if similarity_score > 0.1:  
        most_similar_key = knowledge_base_keys[most_similar_idx]
        most_similar_value = KNOWLEDGE_BASE[most_similar_key]
        return most_similar_key, most_similar_value, similarity_score
    else:
        return None, None, similarity_score


@app.route('/ask', methods=['POST'])
def ask_question():
    # Get question and uploaded file from the request
    question = request.form.get("question", "").strip().lower() 
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
        most_similar_key, most_similar_value, similarity_score = find_most_similar_key(question, KNOWLEDGE_BASE)

        # Set a similarity threshold
        if similarity_score > 0.05:  
            context = most_similar_value
        else:
            context = "No relevant context found for the question."
            
    # Get the response from the chatbot
    response = chatbot.get_response(context, question)
    if response["success"]:
        return jsonify({"answer": response["response"]})
    else:
        return jsonify({"error": response["error"]}), 500


def preprocess_text(text):
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters (optional)
    text = re.sub(r'[^\w\s.,!?]', ' ', text)
    return text.strip()


def extract_relevant_context(text, question):
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


@app.route('/', methods=['GET'])
def home():
    return jsonify("[CONNECTED]")

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json  # Get JSON data from the request
    user_message = data.get("message", "")
    
    # Your chatbot logic here
    bot_response = f"Chatbot response to: {user_message}"
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
