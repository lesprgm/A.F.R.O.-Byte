from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import google.generativeai as genai
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

app = Flask(__name__)
CORS(app)  

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
    system_instruction="You are a friendly teacher that teaches students only about computer science. "
                       "Answer their questions concisely. If a question is outside computer science, do not respond "
                       "and instead ask the user to ask a computer science-related question. "
                       "If your answer is too brief, direct the user to the Learn or Courses page for more details. "
                       "If the user asks you about Afrobyte, say it is a website made by students in the College of Wooster "
                       "to help students learn computer science, of which you, the chatbot, are a part.",
)

@app.route('/chatbot')
def chatbot():
    return render_template('ChatbotPage.html')

@app.route('/<page>')
def serve_page(page):
    if page.endswith('.html'):
        return send_from_directory('.', page)
    return "Page not found", 404

@app.route('/')
def home():
    return send_from_directory('.', 'HomePage.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = model.generate_content(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)