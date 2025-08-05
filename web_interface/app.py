from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
RASA_SERVER_URL = os.getenv('RASA_SERVER_URL', 'http://localhost:5005')
LANGUAGE_DETECTION_ENABLED = os.getenv('LANGUAGE_DETECTION_ENABLED', 'true').lower() == 'true'

@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and communicate with Rasa"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Prepare payload for Rasa
        payload = {
            'sender': session_id,
            'message': user_message
        }
        
        # Send message to Rasa
        rasa_response = requests.post(
            f'{RASA_SERVER_URL}/webhooks/rest/webhook',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if rasa_response.status_code == 200:
            bot_responses = rasa_response.json()
            
            # Extract bot messages
            messages = []
            for response in bot_responses:
                if 'text' in response:
                    messages.append({
                        'type': 'bot',
                        'content': response['text'],
                        'timestamp': response.get('timestamp', '')
                    })
            
            return jsonify({
                'success': True,
                'messages': messages,
                'session_id': session_id
            })
        else:
            return jsonify({
                'error': 'Failed to get response from chatbot',
                'status_code': rasa_response.status_code
            }), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Cannot connect to chatbot server. Please ensure Rasa is running.'
        }), 503
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check if Rasa server is running
        response = requests.get(f'{RASA_SERVER_URL}/status', timeout=5)
        if response.status_code == 200:
            return jsonify({
                'status': 'healthy',
                'rasa_server': 'connected',
                'message': 'All services are running'
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'rasa_server': 'error',
                'message': 'Rasa server returned error'
            }), 503
    except requests.exceptions.RequestException:
        return jsonify({
            'status': 'unhealthy',
            'rasa_server': 'disconnected',
            'message': 'Cannot connect to Rasa server'
        }), 503

@app.route('/api/languages')
def get_supported_languages():
    """Return supported languages"""
    return jsonify({
        'languages': [
            {
                'code': 'en',
                'name': 'English',
                'native_name': 'English'
            },
            {
                'code': 'si',
                'name': 'Sinhala',
                'native_name': 'සිංහල'
            },
            {
                'code': 'ta',
                'name': 'Tamil',
                'native_name': 'தமிழ்'
            }
        ]
    })

@app.route('/api/tourism-info')
def get_tourism_info():
    """Return general tourism information"""
    return jsonify({
        'quick_info': {
            'currency': 'Sri Lankan Rupee (LKR)',
            'timezone': 'UTC+5:30',
            'emergency': '119',
            'tourist_police': '011-242-1052',
            'best_time': 'December to April',
            'capital': 'Colombo'
        },
        'popular_attractions': [
            'Sigiriya',
            'Nuwara Eliya',
            'Galle Fort',
            'Yala National Park',
            'Kandy',
            'Anuradhapura'
        ],
        'popular_foods': [
            'Rice and Curry',
            'Kottu Roti',
            'Hoppers',
            'String Hoppers',
            'Lamprais'
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Starting Sri Lanka Tourism Chatbot Web Interface")
    print(f"📡 Rasa Server URL: {RASA_SERVER_URL}")
    print(f"🌐 Web Interface: http://localhost:{port}")
    print(f"🔧 Debug Mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)