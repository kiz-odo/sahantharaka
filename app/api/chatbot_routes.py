"""
Chatbot API Routes

Provides REST API endpoints for the multilingual tourism chatbot,
including message processing, language detection, and session management.
"""

from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
import logging
import uuid
from datetime import datetime

from ..chatbot import TourismChatbot

logger = logging.getLogger(__name__)

# Create blueprint for chatbot routes
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Initialize chatbot instance
chatbot = TourismChatbot()

@chatbot_bp.route('/chat', methods=['POST'])
@cross_origin()
def process_message():
    """
    Process a user message and return a response.
    
    Expected JSON payload:
    {
        "message": "User message text",
        "user_id": "Unique user identifier",
        "language": "Optional: pre-detected language code"
    }
    
    Returns:
    {
        "response": "Bot response text",
        "language": "Detected language code",
        "intent": "Detected intent",
        "confidence": "Confidence score",
        "entities": "Extracted entities",
        "session_id": "User session ID"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message',
                'status': 'error'
            }), 400
        
        message = data.get('message', '').strip()
        user_id = data.get('user_id', str(uuid.uuid4()))
        detected_language = data.get('language')
        
        if not message:
            return jsonify({
                'error': 'Message cannot be empty',
                'status': 'error'
            }), 400
        
        # Process message through chatbot
        result = chatbot.process_message(
            user_id=user_id,
            message=message,
            detected_language=detected_language
        )
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        result['status'] = 'success'
        
        logger.info(f"Processed message for user {user_id}: {message[:50]}...")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/detect-language', methods=['POST'])
@cross_origin()
def detect_language():
    """
    Detect the language of a text message.
    
    Expected JSON payload:
    {
        "text": "Text to analyze"
    }
    
    Returns:
    {
        "language": "Detected language code",
        "language_name": "Full language name",
        "confidence": "Detection confidence",
        "detection_stats": "Detailed detection statistics"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text',
                'status': 'error'
            }), 400
        
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'error': 'Text cannot be empty',
                'status': 'error'
            }), 400
        
        # Detect language
        language_code = chatbot.language_detector.detect_language(text)
        language_name = chatbot.language_detector.get_language_name(language_code)
        detection_stats = chatbot.language_detector.get_detection_stats(text)
        
        result = {
            'language': language_code,
            'language_name': language_name,
            'confidence': detection_stats.get('final_result') == language_code,
            'detection_stats': detection_stats,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error detecting language: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/user/<user_id>/preferences', methods=['GET'])
@cross_origin()
def get_user_preferences(user_id):
    """
    Get user preferences and settings.
    
    Returns:
    {
        "preferred_language": "User's preferred language",
        "favorites": "List of user's favorite items",
        "session_duration": "Current session duration in seconds"
    }
    """
    try:
        preferences = chatbot.get_user_preferences(user_id)
        
        result = {
            'user_id': user_id,
            'preferences': preferences,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting user preferences: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/user/<user_id>/preferences', methods=['PUT'])
@cross_origin()
def set_user_preference(user_id):
    """
    Set a user preference.
    
    Expected JSON payload:
    {
        "preference": "Preference name",
        "value": "Preference value"
    }
    
    Returns:
    {
        "message": "Preference updated successfully",
        "status": "success"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'preference' not in data or 'value' not in data:
            return jsonify({
                'error': 'Missing required fields: preference and value',
                'status': 'error'
            }), 400
        
        preference = data.get('preference')
        value = data.get('value')
        
        chatbot.set_user_preference(user_id, preference, value)
        
        result = {
            'message': f'Preference {preference} updated successfully',
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error setting user preference: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/user/<user_id>/conversation-summary', methods=['GET'])
@cross_origin()
def get_conversation_summary(user_id):
    """
    Get a summary of the user's conversation.
    
    Returns:
    {
        "total_messages": "Total number of messages",
        "languages_used": "List of languages used",
        "session_start": "Session start timestamp",
        "last_interaction": "Last interaction timestamp",
        "topics_discussed": "List of topics discussed"
    }
    """
    try:
        summary = chatbot.get_conversation_summary(user_id)
        
        result = {
            'user_id': user_id,
            'summary': summary,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting conversation summary: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/user/<user_id>/session', methods=['DELETE'])
@cross_origin()
def reset_user_session(user_id):
    """
    Reset a user's session.
    
    Returns:
    {
        "message": "Session reset successfully",
        "status": "success"
    }
    """
    try:
        chatbot.reset_session(user_id)
        
        result = {
            'message': 'Session reset successfully',
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error resetting user session: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/languages', methods=['GET'])
@cross_origin()
def get_supported_languages():
    """
    Get list of supported languages.
    
    Returns:
    {
        "languages": "List of supported language codes and names",
        "status": "success"
    }
    """
    try:
        languages = chatbot.get_supported_languages()
        language_names = {
            'en': 'English',
            'si': 'Sinhala',
            'ta': 'Tamil'
        }
        
        result = {
            'languages': {code: language_names.get(code, code) for code in languages},
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/intents', methods=['GET'])
@cross_origin()
def get_supported_intents():
    """
    Get list of supported intents.
    
    Returns:
    {
        "intents": "List of supported intents with descriptions",
        "status": "success"
    }
    """
    try:
        intents = chatbot.intent_handler.get_supported_intents()
        intent_descriptions = {}
        
        for intent in intents:
            intent_descriptions[intent] = chatbot.intent_handler.get_intent_description(intent)
        
        result = {
            'intents': intent_descriptions,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting supported intents: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/guide/personality', methods=['GET'])
@cross_origin()
def get_guide_personality():
    """
    Get information about the current tour guide personality.
    
    Returns:
    {
        "guide_name": "Current guide name",
        "personality_traits": "Personality characteristics",
        "conversation_style": "Conversation style elements",
        "status": "success"
    }
    """
    try:
        personality = chatbot.personality.get_personality_summary()
        
        result = {
            'personality': personality,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting guide personality: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/guide/personality', methods=['PUT'])
@cross_origin()
def change_guide_personality():
    """
    Change the tour guide personality.
    
    Expected JSON payload:
    {
        "guide_name": "New guide name ('Saru' or 'Anjali')"
    }
    
    Returns:
    {
        "message": "Guide personality changed successfully",
        "new_guide": "New guide name",
        "status": "success"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'guide_name' not in data:
            return jsonify({
                'error': 'Missing required field: guide_name',
                'status': 'error'
            }), 400
        
        new_guide_name = data.get('guide_name')
        
        if new_guide_name not in ['Saru', 'Anjali']:
            return jsonify({
                'error': 'Invalid guide name. Must be "Saru" or "Anjali"',
                'status': 'error'
            }), 400
        
        chatbot.personality.change_guide(new_guide_name)
        
        result = {
            'message': 'Guide personality changed successfully',
            'new_guide': new_guide_name,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error changing guide personality: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """
    Health check endpoint for the chatbot service.
    
    Returns:
    {
        "status": "healthy",
        "service": "Sri Lanka Tourism Chatbot",
        "version": "1.0.0",
        "timestamp": "Current timestamp"
    }
    """
    try:
        result = {
            'status': 'healthy',
            'service': 'Sri Lanka Tourism Chatbot',
            'version': '1.0.0',
            'supported_languages': chatbot.get_supported_languages(),
            'supported_intents': chatbot.intent_handler.get_supported_intents(),
            'guide_name': chatbot.personality.get_guide_name(),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


# Error handlers
@chatbot_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'timestamp': datetime.now().isoformat()
    }), 404


@chatbot_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'status': 'error',
        'timestamp': datetime.now().isoformat()
    }), 405


@chatbot_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'status': 'error',
        'timestamp': datetime.now().isoformat()
    }), 500