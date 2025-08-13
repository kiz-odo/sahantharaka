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
from ..chatbot.security_manager import SecurityManager, MFAMethod

logger = logging.getLogger(__name__)

# Create blueprint for chatbot routes
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Initialize chatbot instance
chatbot = TourismChatbot()

# Initialize security manager
security_manager = SecurityManager()

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


# MFA Security Routes
@chatbot_bp.route('/security/mfa/setup', methods=['POST'])
@cross_origin()
def setup_mfa():
    """
    Setup MFA for a user.
    
    Expected JSON payload:
    {
        "user_id": "Unique user identifier",
        "method": "totp|sms|email|biometric|backup_codes",
        "additional_data": {
            "phone_number": "Phone number for SMS",
            "email": "Email for email verification"
        }
    }
    
    Returns:
    {
        "status": "success",
        "method": "MFA method",
        "setup_info": "Setup information",
        "instructions": "Setup instructions"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'method' not in data:
            return jsonify({
                'error': 'Missing required fields: user_id, method',
                'status': 'error'
            }), 400
        
        user_id = data.get('user_id')
        method_str = data.get('method')
        additional_data = data.get('additional_data', {})
        
        # Validate MFA method
        try:
            method = MFAMethod(method_str)
        except ValueError:
            return jsonify({
                'error': f'Invalid MFA method: {method_str}',
                'status': 'error'
            }), 400
        
        # Setup MFA
        setup_info = security_manager.setup_mfa(user_id, method, additional_data)
        
        result = {
            'status': 'success',
            'method': method.value,
            'setup_info': setup_info,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"MFA setup initiated for user {user_id} with method {method.value}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error setting up MFA: {str(e)}")
        return jsonify({
            'error': 'MFA setup failed',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/security/mfa/verify', methods=['POST'])
@cross_origin()
def verify_mfa():
    """
    Verify MFA code for a user.
    
    Expected JSON payload:
    {
        "user_id": "Unique user identifier",
        "method": "totp|sms|email|biometric|backup_codes",
        "code": "Verification code",
        "additional_data": "Additional data for verification"
    }
    
    Returns:
    {
        "status": "success|failed",
        "verified": true|false,
        "message": "Verification result message"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'method' not in data or 'code' not in data:
            return jsonify({
                'error': 'Missing required fields: user_id, method, code',
                'status': 'error'
            }), 400
        
        user_id = data.get('user_id')
        method_str = data.get('method')
        code = data.get('code')
        additional_data = data.get('additional_data', {})
        
        # Validate MFA method
        try:
            method = MFAMethod(method_str)
        except ValueError:
            return jsonify({
                'error': f'Invalid MFA method: {method_str}',
                'status': 'error'
            }), 400
        
        # Verify MFA
        is_verified = security_manager.verify_mfa(user_id, method, code, additional_data)
        
        if is_verified:
            result = {
                'status': 'success',
                'verified': True,
                'message': 'MFA verification successful',
                'timestamp': datetime.now().isoformat()
            }
        else:
            result = {
                'status': 'failed',
                'verified': False,
                'message': 'MFA verification failed',
                'timestamp': datetime.now().isoformat()
            }
        
        logger.info(f"MFA verification for user {user_id} with method {method.value}: {'success' if is_verified else 'failed'}")
        
        return jsonify(result), 200 if is_verified else 401
        
    except Exception as e:
        logger.error(f"Error verifying MFA: {str(e)}")
        return jsonify({
            'error': 'MFA verification failed',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/security/mfa/status/<user_id>', methods=['GET'])
@cross_origin()
def get_mfa_status(user_id):
    """
    Get MFA status for a user.
    
    Returns:
    {
        "status": "success",
        "mfa_enabled": true|false,
        "methods": [
            {
                "method": "totp",
                "name": "Time-based One-Time Password",
                "security_level": "high",
                "last_used": "Last used timestamp"
            }
        ],
        "total_methods": 1
    }
    """
    try:
        mfa_status = security_manager.get_user_mfa_status(user_id)
        
        result = {
            'status': 'success',
            'user_id': user_id,
            'mfa_status': mfa_status,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting MFA status for user {user_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to get MFA status',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/security/events', methods=['GET'])
@cross_origin()
def get_security_events():
    """
    Get security events with optional filtering.
    
    Query parameters:
    - user_id: Filter by specific user
    - event_type: Filter by event type
    - limit: Limit number of results (default: 100)
    
    Returns:
    {
        "status": "success",
        "events": [
            {
                "event_id": "Event identifier",
                "user_id": "User identifier",
                "event_type": "Event type",
                "description": "Event description",
                "timestamp": "Event timestamp",
                "severity": "Event severity"
            }
        ],
        "total_events": 10
    }
    """
    try:
        user_id = request.args.get('user_id')
        event_type = request.args.get('event_type')
        limit = int(request.args.get('limit', 100))
        
        events = security_manager.get_security_events(user_id, event_type, limit)
        
        result = {
            'status': 'success',
            'events': events,
            'total_events': len(events),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting security events: {str(e)}")
        return jsonify({
            'error': 'Failed to get security events',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/security/stats', methods=['GET'])
@cross_origin()
def get_security_stats():
    """
    Get security statistics.
    
    Returns:
    {
        "status": "success",
        "stats": {
            "total_users": 100,
            "users_with_mfa": 75,
            "mfa_adoption_rate": 75.0,
            "total_security_events": 150,
            "recent_security_events_24h": 5,
            "locked_users": 2,
            "security_status": "healthy"
        }
    }
    """
    try:
        stats = security_manager.get_security_stats()
        
        result = {
            'status': 'success',
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting security stats: {str(e)}")
        return jsonify({
            'error': 'Failed to get security stats',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/security/mfa/methods', methods=['GET'])
@cross_origin()
def get_mfa_methods():
    """
    Get available MFA methods and their information.
    
    Returns:
    {
        "status": "success",
        "methods": {
            "totp": {
                "name": "Time-based One-Time Password",
                "security_level": "high",
                "user_experience": "good",
                "implementation_effort": "medium",
                "cost": "low"
            }
        }
    }
    """
    try:
        methods_info = {}
        for method, info in security_manager.mfa_methods.items():
            methods_info[method.value] = {
                'name': info['name'],
                'security_level': info['security_level'].value,
                'user_experience': info['user_experience'],
                'implementation_effort': info['implementation_effort'],
                'cost': info['cost']
            }
        
        result = {
            'status': 'success',
            'methods': methods_info,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting MFA methods: {str(e)}")
        return jsonify({
            'error': 'Failed to get MFA methods',
            'status': 'error',
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