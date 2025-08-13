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
from typing import Dict

from ..chatbot import TourismChatbot
from ..chatbot.security_manager import SecurityManager, MFAMethod
from ..chatbot.trip_planner import TripPlanner

logger = logging.getLogger(__name__)

# Create blueprint for chatbot routes
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Initialize chatbot instance
chatbot = TourismChatbot()

# Initialize security manager
security_manager = SecurityManager()

# Initialize trip planner
trip_planner = TripPlanner()

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


# Trip Planning Routes
@chatbot_bp.route('/trip-planning/create', methods=['POST'])
@cross_origin()
def create_trip_plan():
    """
    Create a personalized trip plan based on user preferences.
    
    Expected JSON payload:
    {
        "user_id": "Unique user identifier",
        "trip_type": "cultural|adventure|relaxation|family|budget|luxury|photography|food|nature|historical",
        "budget_level": "budget|moderate|luxury",
        "duration_days": 7,
        "group_size": 2,
        "preferred_season": "peak|shoulder|low",
        "interests": ["culture", "history", "food"],
        "accommodation_type": "hostel|guesthouse|hotel|resort|villa",
        "transport_preference": "public|mix|private",
        "dietary_restrictions": ["vegetarian"],
        "accessibility_requirements": [],
        "language_preference": "en"
    }
    
    Returns:
    {
        "status": "success",
        "trip_id": "Generated trip ID",
        "itinerary": "Complete trip itinerary",
        "recommendations": "Personalized recommendations"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({
                'error': 'Missing required field: user_id',
                'status': 'error'
            }), 400
        
        user_id = data.get('user_id')
        preferences = data.copy()
        
        # Create trip plan
        result = trip_planner.create_trip_plan(user_id, preferences)
        
        if result.get('status') == 'success':
            logger.info(f"Trip plan created successfully for user {user_id}")
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error creating trip plan: {str(e)}")
        return jsonify({
            'error': 'Failed to create trip plan',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/user-trips/<user_id>', methods=['GET'])
@cross_origin()
def get_user_trips(user_id):
    """
    Get all trips for a specific user.
    
    Returns:
    {
        "status": "success",
        "user_id": "User identifier",
        "trips": [
            {
                "trip_id": "Trip identifier",
                "title": "Trip title",
                "start_date": "Start date",
                "end_date": "End date",
                "total_budget": 1500.0,
                "status": "draft"
            }
        ],
        "total_trips": 2
    }
    """
    try:
        trips = trip_planner.get_user_trips(user_id)
        
        result = {
            'status': 'success',
            'user_id': user_id,
            'trips': trips,
            'total_trips': len(trips),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting user trips for {user_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to get user trips',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/trip/<trip_id>', methods=['GET'])
@cross_origin()
def get_trip_details(trip_id):
    """
    Get detailed information about a specific trip.
    
    Returns:
    {
        "status": "success",
        "trip": "Complete trip details"
    }
    """
    try:
        trip = trip_planner.get_trip_details(trip_id)
        
        if trip:
            result = {
                'status': 'success',
                'trip': trip,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(result), 200
        else:
            return jsonify({
                'error': 'Trip not found',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting trip details for {trip_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to get trip details',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/trip/<trip_id>', methods=['PUT'])
@cross_origin()
def update_trip(trip_id):
    """
    Update trip details.
    
    Expected JSON payload:
    {
        "title": "Updated trip title",
        "status": "confirmed",
        "additional_notes": "Updated notes"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Trip updated successfully"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No update data provided',
                'status': 'error'
            }), 400
        
        # Update trip
        success = trip_planner.update_trip(trip_id, data)
        
        if success:
            result = {
                'status': 'success',
                'message': 'Trip updated successfully',
                'trip_id': trip_id,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(result), 200
        else:
            return jsonify({
                'error': 'Trip not found or update failed',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 404
            
    except Exception as e:
        logger.error(f"Error updating trip {trip_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to update trip',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/trip/<trip_id>', methods=['DELETE'])
@cross_origin()
def delete_trip(trip_id):
    """
    Delete a trip.
    
    Returns:
    {
        "status": "success",
        "message": "Trip deleted successfully"
    }
    """
    try:
        # Delete trip
        success = trip_planner.delete_trip(trip_id)
        
        if success:
            result = {
                'status': 'success',
                'message': 'Trip deleted successfully',
                'trip_id': trip_id,
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(result), 200
        else:
            return jsonify({
                'error': 'Trip not found or deletion failed',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 404
            
    except Exception as e:
        logger.error(f"Error deleting trip {trip_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to delete trip',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/templates', methods=['GET'])
@cross_origin()
def get_trip_templates():
    """
    Get available trip templates.
    
    Returns:
    {
        "status": "success",
        "templates": [
            {
                "type": "cultural",
                "name": "Cultural Heritage Tour",
                "description": "Explore Sri Lanka's rich cultural heritage"
            }
        ]
    }
    """
    try:
        templates = trip_planner.trip_templates
        
        result = {
            'status': 'success',
            'templates': [
                {
                    'type': template_type,
                    'name': template.get('name', ''),
                    'description': template.get('description', '')
                }
                for template_type, template in templates.items()
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting trip templates: {str(e)}")
        return jsonify({
            'error': 'Failed to get trip templates',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/options', methods=['GET'])
@cross_origin()
def get_trip_planning_options():
    """
    Get all available options for trip planning.
    
    Returns:
    {
        "status": "success",
        "trip_types": ["cultural", "adventure", "relaxation"],
        "budget_levels": ["budget", "moderate", "luxury"],
        "seasons": ["peak", "shoulder", "low"],
        "accommodation_types": ["hostel", "guesthouse", "hotel"],
        "transport_preferences": ["public", "mix", "private"]
    }
    """
    try:
        result = {
            'status': 'success',
            'trip_types': [
                'cultural', 'adventure', 'relaxation', 'family', 'budget',
                'luxury', 'photography', 'food', 'nature', 'historical'
            ],
            'budget_levels': ['budget', 'moderate', 'luxury'],
            'seasons': ['peak', 'shoulder', 'low'],
            'accommodation_types': ['hostel', 'guesthouse', 'hotel', 'resort', 'villa'],
            'transport_preferences': ['public', 'mix', 'private'],
            'common_interests': [
                'culture', 'history', 'nature', 'adventure', 'food', 'photography',
                'shopping', 'wellness', 'education', 'relaxation'
            ],
            'dietary_options': [
                'vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'halal', 'kosher'
            ],
            'accessibility_options': [
                'wheelchair-accessible', 'mobility-assistance', 'visual-aids', 'hearing-aids'
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error getting trip planning options: {str(e)}")
        return jsonify({
            'error': 'Failed to get trip planning options',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/quick-plan', methods=['POST'])
@cross_origin()
def create_quick_trip_plan():
    """
    Create a quick trip plan with minimal preferences.
    
    Expected JSON payload:
    {
        "user_id": "Unique user identifier",
        "trip_type": "cultural",
        "duration_days": 5,
        "budget_level": "moderate"
    }
    
    Returns:
    {
        "status": "success",
        "trip_id": "Generated trip ID",
        "itinerary": "Quick trip itinerary"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({
                'error': 'Missing required field: user_id',
                'status': 'error'
            }), 400
        
        # Set default values for quick plan
        quick_preferences = {
            'user_id': data['user_id'],
            'trip_type': data.get('trip_type', 'cultural'),
            'budget_level': data.get('budget_level', 'moderate'),
            'duration_days': data.get('duration_days', 5),
            'group_size': 2,
            'preferred_season': 'peak',
            'interests': ['culture', 'history'],
            'accommodation_type': 'hotel',
            'transport_preference': 'mix',
            'dietary_restrictions': [],
            'accessibility_requirements': [],
            'language_preference': 'en'
        }
        
        # Create quick trip plan
        result = trip_planner.create_trip_plan(data['user_id'], quick_preferences)
        
        if result.get('status') == 'success':
            logger.info(f"Quick trip plan created for user {data['user_id']}")
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error creating quick trip plan: {str(e)}")
        return jsonify({
            'error': 'Failed to create quick trip plan',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


@chatbot_bp.route('/trip-planning/export/<trip_id>', methods=['GET'])
@cross_origin()
def export_trip_plan(trip_id):
    """
    Export trip plan in various formats.
    
    Query parameters:
    - format: pdf|json|html (default: json)
    
    Returns:
    Trip plan in the requested format
    """
    try:
        format_type = request.args.get('format', 'json')
        
        # Get trip details
        trip = trip_planner.get_trip_details(trip_id)
        
        if not trip:
            return jsonify({
                'error': 'Trip not found',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 404
        
        if format_type == 'json':
            return jsonify({
                'status': 'success',
                'trip': trip,
                'export_format': 'json',
                'timestamp': datetime.now().isoformat()
            }), 200
        elif format_type == 'html':
            # Generate HTML export
            html_content = _generate_trip_html(trip)
            return html_content, 200, {'Content-Type': 'text/html'}
        elif format_type == 'pdf':
            # For PDF export, you would need additional libraries
            return jsonify({
                'error': 'PDF export not yet implemented',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 501
        else:
            return jsonify({
                'error': 'Unsupported export format',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }), 400
            
    except Exception as e:
        logger.error(f"Error exporting trip plan {trip_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to export trip plan',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500


def _generate_trip_html(trip: Dict) -> str:
    """Generate HTML export for trip plan."""
    try:
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{trip.get('title', 'Trip Plan')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .trip-info {{ margin-bottom: 20px; }}
                .day-plan {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; }}
                .activity {{ margin-bottom: 10px; }}
                .budget {{ background: #f9f9f9; padding: 10px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{trip.get('title', 'Trip Plan')}</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="trip-info">
                <h2>Trip Information</h2>
                <p><strong>Duration:</strong> {trip.get('preferences', {}).get('duration_days', 0)} days</p>
                <p><strong>Budget Level:</strong> {trip.get('preferences', {}).get('budget_level', 'moderate')}</p>
                <p><strong>Group Size:</strong> {trip.get('preferences', {}).get('group_size', 0)} people</p>
                <p><strong>Total Budget:</strong> ${trip.get('total_budget', 0):.2f}</p>
            </div>
        """
        
        # Add daily plans
        for day_plan in trip.get('daily_itineraries', []):
            html += f"""
            <div class="day-plan">
                <h3>Day {day_plan.get('day_number', 0)} - {day_plan.get('location', 'Unknown')}</h3>
                <p><strong>Estimated Cost:</strong> ${day_plan.get('estimated_cost', 0):.2f}</p>
                
                <h4>Activities:</h4>
            """
            
            for activity in day_plan.get('activities', []):
                html += f"""
                <div class="activity">
                    <strong>{activity.get('name', 'Activity')}</strong><br>
                    {activity.get('description', '')}<br>
                    Duration: {activity.get('duration', '')} | Cost: ${activity.get('cost', 0)}
                </div>
                """
            
            html += """
                </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
        
    except Exception as e:
        logger.error(f"Error generating trip HTML: {str(e)}")
        return f"<html><body><h1>Error generating trip plan</h1><p>{str(e)}</p></body></html>"


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