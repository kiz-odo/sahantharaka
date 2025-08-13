"""
Chatbot API Routes for Sri Lanka Tourism

Provides RESTful API endpoints for the multilingual tourism chatbot
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import uuid

# Import chatbot components
from app.chatbot import TourismChatbot

logger = logging.getLogger(__name__)

# Create blueprint for chatbot routes
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Initialize the chatbot instance
chatbot = TourismChatbot()

@chatbot_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for chatbot service"""
    return jsonify({
        'status': 'healthy',
        'service': 'Sri Lanka Tourism Chatbot API',
        'timestamp': datetime.now().isoformat(),
        'supported_languages': chatbot.get_supported_languages(),
        'available_guides': list(chatbot.get_available_guides().keys())
    })

@chatbot_bp.route('/session/create', methods=['POST'])
def create_session():
    """Create a new chatbot session"""
    try:
        data = request.get_json() or {}
        
        # Generate user ID if not provided
        user_id = data.get('user_id', str(uuid.uuid4()))
        language = data.get('language', 'en')
        
        # Validate language
        if not chatbot.language_detector.is_supported_language(language):
            return jsonify({
                'error': 'Unsupported language',
                'supported_languages': chatbot.get_supported_languages()
            }), 400
        
        # Create session
        session_id = chatbot.create_session(user_id, language)
        
        # Get initial greeting
        greeting_response = chatbot.process_message(session_id, "hello")
        
        return jsonify({
            'session_id': session_id,
            'user_id': user_id,
            'language': language,
            'greeting': greeting_response,
            'available_guides': chatbot.get_available_guides(),
            'created_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return jsonify({
            'error': 'Failed to create session',
            'message': str(e)
        }), 500

@chatbot_bp.route('/message', methods=['POST'])
def process_message():
    """Process user message and return chatbot response"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        session_id = data.get('session_id')
        message = data.get('message')
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process message
        response = chatbot.process_message(session_id, message)
        
        if 'error' in response:
            return jsonify(response), 400
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            'error': 'Failed to process message',
            'message': str(e)
        }), 500

@chatbot_bp.route('/session/<session_id>', methods=['GET'])
def get_session_info(session_id):
    """Get session information"""
    try:
        session_info = chatbot.get_session_info(session_id)
        
        if not session_info:
            return jsonify({'error': 'Session not found'}), 404
        
        # Remove sensitive information
        safe_session_info = {
            'session_id': session_id,
            'user_id': session_info['user_id'],
            'language': session_info['language'],
            'guide': session_info['guide'],
            'created_at': session_info['created_at'].isoformat(),
            'conversation_count': len(session_info.get('conversation_history', []))
        }
        
        return jsonify(safe_session_info)
        
    except Exception as e:
        logger.error(f"Error getting session info: {str(e)}")
        return jsonify({
            'error': 'Failed to get session info',
            'message': str(e)
        }), 500

@chatbot_bp.route('/session/<session_id>/history', methods=['GET'])
def get_conversation_history(session_id):
    """Get conversation history for a session"""
    try:
        history = chatbot.get_conversation_history(session_id)
        
        if history is None:
            return jsonify({'error': 'Session not found'}), 404
        
        # Format history for API response
        formatted_history = []
        for entry in history:
            formatted_entry = {
                'timestamp': entry['timestamp'].isoformat(),
                'user_message': entry['user_message'],
                'response': entry['response'],
                'language': entry['detected_language'],
                'intent': entry['intent'],
                'entities': entry['entities']
            }
            formatted_history.append(formatted_entry)
        
        return jsonify({
            'session_id': session_id,
            'conversation_history': formatted_history,
            'total_messages': len(formatted_history)
        })
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {str(e)}")
        return jsonify({
            'error': 'Failed to get conversation history',
            'message': str(e)
        }), 500

@chatbot_bp.route('/session/<session_id>/language', methods=['PUT'])
def switch_language(session_id):
    """Switch session language"""
    try:
        data = request.get_json()
        
        if not data or 'language' not in data:
            return jsonify({'error': 'Language is required'}), 400
        
        language = data['language']
        
        success = chatbot.switch_language(session_id, language)
        
        if not success:
            return jsonify({
                'error': 'Failed to switch language',
                'supported_languages': chatbot.get_supported_languages()
            }), 400
        
        return jsonify({
            'session_id': session_id,
            'language': language,
            'message': 'Language switched successfully'
        })
        
    except Exception as e:
        logger.error(f"Error switching language: {str(e)}")
        return jsonify({
            'error': 'Failed to switch language',
            'message': str(e)
        }), 500

@chatbot_bp.route('/session/<session_id>/guide', methods=['PUT'])
def switch_guide(session_id):
    """Switch virtual tour guide"""
    try:
        data = request.get_json()
        
        if not data or 'guide' not in data:
            return jsonify({'error': 'Guide is required'}), 400
        
        guide = data['guide']
        
        success = chatbot.switch_guide(session_id, guide)
        
        if not success:
            return jsonify({
                'error': 'Failed to switch guide',
                'available_guides': list(chatbot.get_available_guides().keys())
            }), 400
        
        return jsonify({
            'session_id': session_id,
            'guide': guide,
            'message': 'Guide switched successfully'
        })
        
    except Exception as e:
        logger.error(f"Error switching guide: {str(e)}")
        return jsonify({
            'error': 'Failed to switch guide',
            'message': str(e)
        }), 500

@chatbot_bp.route('/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    try:
        languages = chatbot.get_supported_languages()
        
        # Add additional info for each language
        detailed_languages = {}
        for code, name in languages.items():
            lang_info = chatbot.language_detector.get_language_info(code)
            detailed_languages[code] = {
                'name': name,
                'code': code,
                'supported_features': lang_info['supported_features'] if lang_info else []
            }
        
        return jsonify({
            'supported_languages': detailed_languages,
            'default_language': chatbot.default_language
        })
        
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        return jsonify({
            'error': 'Failed to get supported languages',
            'message': str(e)
        }), 500

@chatbot_bp.route('/guides', methods=['GET'])
def get_available_guides():
    """Get list of available tour guides"""
    try:
        guides = chatbot.get_available_guides()
        
        # Format guide information for API response
        formatted_guides = {}
        for guide_id, guide_info in guides.items():
            formatted_guides[guide_id] = {
                'id': guide_id,
                'name': guide_info['name'],
                'gender': guide_info['gender'],
                'personality': guide_info['personality'],
                'specialties': guide_info['specialties'],
                'greeting_preview': guide_info['greeting'].get('en', '')
            }
        
        return jsonify({
            'available_guides': formatted_guides
        })
        
    except Exception as e:
        logger.error(f"Error getting available guides: {str(e)}")
        return jsonify({
            'error': 'Failed to get available guides',
            'message': str(e)
        }), 500

@chatbot_bp.route('/detect-language', methods=['POST'])
def detect_language():
    """Detect language of input text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        
        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Detect language
        detected_lang, confidence = chatbot.language_detector.detect_language(text)
        
        return jsonify({
            'text': text,
            'detected_language': detected_lang,
            'language_name': chatbot.language_detector.language_names[detected_lang],
            'confidence': confidence,
            'supported_languages': chatbot.get_supported_languages()
        })
        
    except Exception as e:
        logger.error(f"Error detecting language: {str(e)}")
        return jsonify({
            'error': 'Failed to detect language',
            'message': str(e)
        }), 500

@chatbot_bp.route('/recognize-intent', methods=['POST'])
def recognize_intent():
    """Recognize intent from input text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        language = data.get('language', 'en')
        
        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Validate language
        if not chatbot.language_detector.is_supported_language(language):
            return jsonify({
                'error': 'Unsupported language',
                'supported_languages': chatbot.get_supported_languages()
            }), 400
        
        # Recognize intent and extract entities
        intent, confidence = chatbot.intent_recognizer.recognize_intent(text, language)
        entities = chatbot.intent_recognizer.extract_entities(text, intent)
        
        return jsonify({
            'text': text,
            'language': language,
            'intent': intent,
            'intent_confidence': confidence,
            'entities': entities,
            'supported_intents': chatbot.intent_recognizer.get_supported_intents()
        })
        
    except Exception as e:
        logger.error(f"Error recognizing intent: {str(e)}")
        return jsonify({
            'error': 'Failed to recognize intent',
            'message': str(e)
        }), 500

@chatbot_bp.route('/search', methods=['POST'])
def search_knowledge_base():
    """Search the tourism knowledge base"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        language = data.get('language', 'en')
        
        if not query.strip():
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Validate language
        if not chatbot.language_detector.is_supported_language(language):
            return jsonify({
                'error': 'Unsupported language',
                'supported_languages': chatbot.get_supported_languages()
            }), 400
        
        # Search knowledge base
        results = chatbot.knowledge_base.search_knowledge_base(query, language)
        
        return jsonify({
            'query': query,
            'language': language,
            'results': results,
            'total_results': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        return jsonify({
            'error': 'Failed to search knowledge base',
            'message': str(e)
        }), 500

@chatbot_bp.route('/emergency-info', methods=['GET'])
def get_emergency_info():
    """Get emergency contact information"""
    try:
        info_type = request.args.get('type', 'all')
        
        emergency_info = chatbot.knowledge_base.get_emergency_info(info_type)
        
        return jsonify({
            'emergency_info': emergency_info,
            'type': info_type
        })
        
    except Exception as e:
        logger.error(f"Error getting emergency info: {str(e)}")
        return jsonify({
            'error': 'Failed to get emergency info',
            'message': str(e)
        }), 500

@chatbot_bp.route('/stats', methods=['GET'])
def get_chatbot_stats():
    """Get chatbot usage statistics"""
    try:
        total_sessions = len(chatbot.sessions)
        active_sessions = sum(1 for session in chatbot.sessions.values() 
                            if len(session.get('conversation_history', [])) > 0)
        
        # Language distribution
        language_distribution = {}
        for session in chatbot.sessions.values():
            lang = session.get('language', 'en')
            language_distribution[lang] = language_distribution.get(lang, 0) + 1
        
        # Guide distribution
        guide_distribution = {}
        for session in chatbot.sessions.values():
            guide = session.get('guide', 'saru')
            guide_distribution[guide] = guide_distribution.get(guide, 0) + 1
        
        return jsonify({
            'total_sessions': total_sessions,
            'active_sessions': active_sessions,
            'language_distribution': language_distribution,
            'guide_distribution': guide_distribution,
            'supported_languages': list(chatbot.get_supported_languages().keys()),
            'available_guides': list(chatbot.get_available_guides().keys()),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting chatbot stats: {str(e)}")
        return jsonify({
            'error': 'Failed to get chatbot stats',
            'message': str(e)
        }), 500

# Error handlers
@chatbot_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@chatbot_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@chatbot_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500