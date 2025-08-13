"""
Main Tourism Chatbot Class

Handles multilingual conversations, language detection, and tourism information
queries in Sinhala, Tamil, and English.
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .language_detector import LanguageDetector
from .tourism_knowledge import TourismKnowledgeBase
from .intents import IntentHandler
from .personality import TourGuidePersonality

logger = logging.getLogger(__name__)


class TourismChatbot:
    """
    Multilingual tourism chatbot for Sri Lanka with personality-driven responses.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the tourism chatbot.
        
        Args:
            config: Configuration dictionary for the chatbot
        """
        self.config = config or {}
        self.language_detector = LanguageDetector()
        self.knowledge_base = TourismKnowledgeBase()
        self.intent_handler = IntentHandler()
        self.personality = TourGuidePersonality()
        
        # User session management
        self.user_sessions = {}
        
        # Supported languages
        self.supported_languages = ['en', 'si', 'ta']  # English, Sinhala, Tamil
        
        logger.info("Tourism Chatbot initialized successfully")
    
    def process_message(self, user_id: str, message: str, 
                       detected_language: str = None) -> Dict:
        """
        Process a user message and return a response.
        
        Args:
            user_id: Unique identifier for the user
            message: User's message text
            detected_language: Pre-detected language (optional)
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Get or create user session
            session = self._get_user_session(user_id)
            
            # Detect language if not provided
            if not detected_language:
                detected_language = self.language_detector.detect_language(message)
            
            # Update session with detected language
            session['current_language'] = detected_language
            session['last_interaction'] = datetime.now()
            
            # Detect intent and entities
            intent_result = self.intent_handler.detect_intent(
                message, detected_language
            )
            
            # Generate response based on intent
            response = self._generate_response(
                intent_result, detected_language, session
            )
            
            # Update session with conversation history
            self._update_session_history(session, message, response)
            
            return {
                'response': response,
                'language': detected_language,
                'intent': intent_result.get('intent'),
                'confidence': intent_result.get('confidence', 0.0),
                'entities': intent_result.get('entities', []),
                'session_id': session['session_id']
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return self._get_error_response(detected_language or 'en')
    
    def _get_user_session(self, user_id: str) -> Dict:
        """Get or create a user session."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'session_id': f"session_{user_id}_{datetime.now().timestamp()}",
                'user_id': user_id,
                'current_language': 'en',
                'preferred_language': 'en',
                'conversation_history': [],
                'favorites': [],
                'last_interaction': datetime.now(),
                'created_at': datetime.now()
            }
        return self.user_sessions[user_id]
    
    def _generate_response(self, intent_result: Dict, 
                          language: str, session: Dict) -> str:
        """Generate a contextual response based on intent and personality."""
        intent = intent_result.get('intent', 'unknown')
        entities = intent_result.get('entities', [])
        
        # Get base response from knowledge base
        base_response = self.knowledge_base.get_response(
            intent, language, entities
        )
        
        # Apply personality and contextualization
        personalized_response = self.personality.personalize_response(
            base_response, intent, language, session
        )
        
        return personalized_response
    
    def _update_session_history(self, session: Dict, 
                               user_message: str, bot_response: str):
        """Update session with conversation history."""
        session['conversation_history'].append({
            'timestamp': datetime.now(),
            'user_message': user_message,
            'bot_response': bot_response,
            'language': session['current_language']
        })
        
        # Keep only last 50 messages to prevent memory issues
        if len(session['conversation_history']) > 50:
            session['conversation_history'] = session['conversation_history'][-50:]
    
    def _get_error_response(self, language: str) -> str:
        """Get an error response in the specified language."""
        error_responses = {
            'en': "I apologize, but I'm having trouble understanding. Could you please rephrase your question?",
            'si': "මට සමාවෙන්න, මට ඔබේ ප්‍රශ්නය තේරුම්ගත නොහැකිය. කරුණාකර ඔබේ ප්‍රශ්නය නැවත ප්‍රකාශ කරන්න?",
            'ta': "மன்னிக்கவும், உங்கள் கேள்வியை புரிந்துகொள்ள முடியவில்லை. தயவுசெய்து உங்கள் கேள்வியை மீண்டும் கேள்விப்படுத்தவும்?"
        }
        return error_responses.get(language, error_responses['en'])
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences and settings."""
        session = self.user_sessions.get(user_id, {})
        return {
            'preferred_language': session.get('preferred_language', 'en'),
            'favorites': session.get('favorites', []),
            'session_duration': (datetime.now() - session.get('created_at', datetime.now())).total_seconds() if session else 0
        }
    
    def set_user_preference(self, user_id: str, preference: str, value: str):
        """Set a user preference."""
        if user_id in self.user_sessions:
            self.user_sessions[user_id][preference] = value
    
    def get_conversation_summary(self, user_id: str) -> Dict:
        """Get a summary of the user's conversation."""
        session = self.user_sessions.get(user_id, {})
        history = session.get('conversation_history', [])
        
        return {
            'total_messages': len(history),
            'languages_used': list(set(msg.get('language', 'en') for msg in history)),
            'session_start': session.get('created_at'),
            'last_interaction': session.get('last_interaction'),
            'topics_discussed': self._extract_topics(history)
        }
    
    def _extract_topics(self, history: List[Dict]) -> List[str]:
        """Extract main topics from conversation history."""
        topics = []
        for msg in history:
            # Simple topic extraction based on keywords
            if any(word in msg.get('user_message', '').lower() for word in ['hotel', 'accommodation']):
                topics.append('accommodation')
            elif any(word in msg.get('user_message', '').lower() for word in ['food', 'restaurant', 'cuisine']):
                topics.append('food')
            elif any(word in msg.get('user_message', '').lower() for word in ['transport', 'bus', 'train']):
                topics.append('transport')
            elif any(word in msg.get('user_message', '').lower() for word in ['attraction', 'place', 'visit']):
                topics.append('attractions')
        
        return list(set(topics))
    
    def reset_session(self, user_id: str):
        """Reset a user's session."""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return self.supported_languages.copy()