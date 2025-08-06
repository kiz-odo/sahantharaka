from flask import Flask, request, jsonify
from langdetect import detect
import requests

app = Flask(__name__)

# Helper function to detect language
def detect_language(text):
    try:
        lang = detect(text)
        if lang == 'en':
            return 'english'
        elif lang == 'si':
            return 'sinhala'
        elif lang == 'ta':
            return 'tamil'
        else:
            return 'unknown'
    except Exception:
        return 'unknown'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    user_lang = detect_language(user_message)
    # Forward message and language to Rasa (assumes Rasa server is running on localhost:5005)
    payload = {
        "sender": "user",
        "message": user_message,
        "metadata": {"lang": user_lang}
    }
    rasa_response = requests.post('http://localhost:5005/webhooks/rest/webhook', json=payload)
    return jsonify({
        "response": rasa_response.json(),
        "detected_language": user_lang
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)