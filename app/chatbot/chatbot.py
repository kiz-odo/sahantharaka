"""
Main Tourism Chatbot for Sri Lanka

Orchestrates all chatbot components and provides multilingual conversational interface
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from .language_detector import LanguageDetector
from .knowledge_base import TourismKnowledgeBase
from .intent_recognizer import IntentRecognizer

logger = logging.getLogger(__name__)

class TourismChatbot:
    """
    Main tourism chatbot class that orchestrates all components
    Provides multilingual conversational interface for Sri Lanka tourism
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the tourism chatbot
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration dictionary
        """
        self.config = config or {}
        
        # Initialize core components
        self.language_detector = LanguageDetector()
        self.knowledge_base = TourismKnowledgeBase()
        self.intent_recognizer = IntentRecognizer()
        
        # Initialize conversation state
        self.sessions = {}
        
        # Initialize virtual tour guides
        self.tour_guides = self._initialize_tour_guides()
        
        # Default configuration
        self.default_language = self.config.get('default_language', 'en')
        self.response_style = self.config.get('response_style', 'friendly')
        
        logger.info("Tourism Chatbot initialized successfully")
    
    def _initialize_tour_guides(self) -> Dict[str, Any]:
        """Initialize virtual tour guide personalities"""
        return {
            'saru': {
                'name': 'Saru',
                'gender': 'female',
                'personality': 'friendly, enthusiastic, cultural expert',
                'specialties': ['temples', 'cultural sites', 'festivals', 'etiquette'],
                'greeting': {
                    'en': "Hello! I'm Saru, your friendly Sri Lankan tour guide! I love sharing our beautiful culture and history.",
                    'si': "ආයුබෝවන්! මම සරු, ඔබේ මිත්‍රශීලී ශ්‍රී ලාංකික ගමන් මාර්ගදර්ශකයා! අපේ සුන්දර සංස්කෘතිය සහ ඉතිහාසය බෙදා ගැනීමට මම ආදරෙයි.",
                    'ta': "வணக்கம்! நான் சரு, உங்கள் நட்புரீதியான இலங்கை சுற்றுலா வழிகாட்டி! எங்கள் அழகான கலாச்சாரம் மற்றும் வரலாற்றைப் பகிர்ந்து கொள்ள நான் விரும்புகிறேன்.",
                    'zh': "你好！我是萨鲁，你友好的斯里兰卡导游！我喜欢分享我们美丽的文化和历史。",
                    'fr': "Bonjour! Je suis Saru, votre guide touristique sri-lankaise amicale! J'adore partager notre belle culture et histoire."
                }
            },
            'anjali': {
                'name': 'Anjali',
                'gender': 'female',
                'personality': 'adventurous, nature-loving, practical',
                'specialties': ['nature', 'wildlife', 'trekking', 'beaches'],
                'greeting': {
                    'en': "Hi there! I'm Anjali, and I'm passionate about Sri Lanka's incredible nature and wildlife!",
                    'si': "හෙලෝ! මම අංජලි, ශ්‍රී ලංකාවේ විස්මයජනක ස්වභාවික පරිසරය සහ වන්‍යජීවීන් ගැන ඉතා උනන්දුයි!",
                    'ta': "வணக்கம்! நான் அஞ்சலி, இலங்கையின் நம்பமுடியாத இயற்கை மற்றும் வனவிலங்குகள் மீது நான் ஆர்வமாக உள்ளேன்!",
                    'zh': "嗨！我是安贾莉，我对斯里兰卡令人难以置信的自然和野生动物充满热情！",
                    'fr': "Salut! Je suis Anjali, et je suis passionnée par la nature et la faune incroyables du Sri Lanka!"
                }
            }
        }
    
    def create_session(self, user_id: str, language: str = None) -> str:
        """
        Create a new conversation session
        
        Args:
            user_id (str): Unique user identifier
            language (str): Preferred language (optional)
            
        Returns:
            str: Session ID
        """
        session_id = f"{user_id}_{datetime.now().timestamp()}"
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'language': language or self.default_language,
            'guide': 'saru',  # Default guide
            'conversation_history': [],
            'context': {},
            'preferences': {}
        }
        
        logger.info(f"Created new session: {session_id} for user: {user_id}")
        return session_id
    
    def process_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Process user message and generate response
        
        Args:
            session_id (str): Session identifier
            message (str): User message
            
        Returns:
            Dict[str, Any]: Response with text, metadata, and suggestions
        """
        if session_id not in self.sessions:
            return {
                'error': 'Invalid session ID',
                'response': 'Session not found. Please start a new conversation.',
                'language': self.default_language
            }
        
        session = self.sessions[session_id]
        
        try:
            # Detect language
            detected_lang, lang_confidence = self.language_detector.detect_language(message)
            
            # Update session language if detection confidence is high
            if lang_confidence > 0.7:
                session['language'] = detected_lang
            
            # Recognize intent
            intent, intent_confidence = self.intent_recognizer.recognize_intent(
                message, session['language']
            )
            
            # Extract entities
            entities = self.intent_recognizer.extract_entities(message, intent)
            
            # Generate response
            response = self._generate_response(session, message, intent, entities)
            
            # Update conversation history
            session['conversation_history'].append({
                'timestamp': datetime.now(),
                'user_message': message,
                'detected_language': detected_lang,
                'intent': intent,
                'entities': entities,
                'response': response['response']
            })
            
            # Add response metadata
            response.update({
                'session_id': session_id,
                'language': session['language'],
                'detected_language': detected_lang,
                'language_confidence': lang_confidence,
                'intent': intent,
                'intent_confidence': intent_confidence,
                'entities': entities,
                'guide': session['guide'],
                'timestamp': datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                'error': 'Processing error',
                'response': self._get_error_response(session['language']),
                'language': session['language']
            }
    
    def _generate_response(self, session: Dict[str, Any], message: str, 
                         intent: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Generate appropriate response based on intent and entities
        
        Args:
            session (Dict[str, Any]): Session data
            message (str): User message
            intent (str): Recognized intent
            entities (Dict[str, List[str]]): Extracted entities
            
        Returns:
            Dict[str, Any]: Response data
        """
        language = session['language']
        guide = session['guide']
        
        if intent == 'greeting':
            return self._handle_greeting(language, guide)
        elif intent == 'attraction_inquiry':
            return self._handle_attraction_inquiry(language, entities)
        elif intent == 'food_inquiry':
            return self._handle_food_inquiry(language, entities)
        elif intent == 'transport_inquiry':
            return self._handle_transport_inquiry(language, entities)
        elif intent == 'accommodation_inquiry':
            return self._handle_accommodation_inquiry(language, entities)
        elif intent == 'weather_inquiry':
            return self._handle_weather_inquiry(language, entities)
        elif intent == 'help_inquiry':
            return self._handle_help_inquiry(language)
        elif intent == 'goodbye':
            return self._handle_goodbye(language, guide)
        else:
            return self._handle_unknown_intent(language, message)
    
    def _handle_greeting(self, language: str, guide: str) -> Dict[str, Any]:
        """Handle greeting intent"""
        guide_info = self.tour_guides[guide]
        greeting = guide_info['greeting'].get(language, guide_info['greeting']['en'])
        
        suggestions = self._get_greeting_suggestions(language)
        
        return {
            'response': greeting,
            'response_type': 'greeting',
            'suggestions': suggestions,
            'quick_replies': self._get_quick_replies(language, 'greeting')
        }
    
    def _handle_attraction_inquiry(self, language: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Handle attraction inquiry intent"""
        response_parts = []
        suggestions = []
        
        # Check if specific locations were mentioned
        locations = entities.get('locations', [])
        
        if locations:
            for location in locations:
                attraction_info = self.knowledge_base.get_attraction_info(location, language)
                if attraction_info:
                    response_parts.append(self._format_attraction_info(attraction_info, language))
                    suggestions.extend(self._get_attraction_suggestions(language))
        
        if not response_parts:
            # General attraction recommendations
            response_parts.append(self._get_general_attractions_response(language))
            suggestions = self._get_attraction_suggestions(language)
        
        return {
            'response': '\n\n'.join(response_parts),
            'response_type': 'attraction_info',
            'suggestions': suggestions[:5],  # Limit to 5 suggestions
            'quick_replies': self._get_quick_replies(language, 'attractions')
        }
    
    def _handle_food_inquiry(self, language: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Handle food inquiry intent"""
        food_info = self.knowledge_base.get_food_info('rice_curry', language)
        
        response = self._get_food_response(language, food_info)
        suggestions = self._get_food_suggestions(language)
        
        return {
            'response': response,
            'response_type': 'food_info',
            'suggestions': suggestions,
            'quick_replies': self._get_quick_replies(language, 'food')
        }
    
    def _handle_transport_inquiry(self, language: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Handle transport inquiry intent"""
        transport_info = self.knowledge_base.get_transport_info('train', language)
        
        response = self._get_transport_response(language, transport_info)
        suggestions = self._get_transport_suggestions(language)
        
        return {
            'response': response,
            'response_type': 'transport_info',
            'suggestions': suggestions,
            'quick_replies': self._get_quick_replies(language, 'transport')
        }
    
    def _handle_accommodation_inquiry(self, language: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Handle accommodation inquiry intent"""
        response = self._get_accommodation_response(language)
        suggestions = self._get_accommodation_suggestions(language)
        
        return {
            'response': response,
            'response_type': 'accommodation_info',
            'suggestions': suggestions,
            'quick_replies': self._get_quick_replies(language, 'accommodation')
        }
    
    def _handle_weather_inquiry(self, language: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Handle weather inquiry intent"""
        response = self._get_weather_response(language)
        suggestions = self._get_weather_suggestions(language)
        
        return {
            'response': response,
            'response_type': 'weather_info',
            'suggestions': suggestions,
            'quick_replies': self._get_quick_replies(language, 'weather')
        }
    
    def _handle_help_inquiry(self, language: str) -> Dict[str, Any]:
        """Handle help inquiry intent"""
        response = self._get_help_response(language)
        suggestions = self._get_help_suggestions(language)
        
        return {
            'response': response,
            'response_type': 'help_info',
            'suggestions': suggestions,
            'quick_replies': self._get_quick_replies(language, 'help')
        }
    
    def _handle_goodbye(self, language: str, guide: str) -> Dict[str, Any]:
        """Handle goodbye intent"""
        response = self._get_goodbye_response(language, guide)
        
        return {
            'response': response,
            'response_type': 'goodbye',
            'suggestions': [],
            'quick_replies': []
        }
    
    def _handle_unknown_intent(self, language: str, message: str) -> Dict[str, Any]:
        """Handle unknown intent"""
        # Try to search knowledge base
        search_results = self.knowledge_base.search_knowledge_base(message, language)
        
        if search_results:
            response = self._format_search_results(search_results, language)
        else:
            response = self._get_unknown_response(language)
        
        suggestions = self._get_general_suggestions(language)
        
        return {
            'response': response,
            'response_type': 'unknown',
            'suggestions': suggestions,
            'quick_replies': self._get_quick_replies(language, 'general')
        }
    
    def _format_attraction_info(self, info: Dict[str, Any], language: str) -> str:
        """Format attraction information for display"""
        if language == 'en':
            return f"**{info['name']}**\n\n{info['description']}\n\n📍 **Location:** {info['location']}\n⏰ **Best time:** {info['best_time']}\n🎫 **Entry fee:** {info['entry_fee']}\n💡 **Tips:** {info['tips']}"
        elif language == 'si':
            return f"**{info['name']}**\n\n{info['description']}\n\n📍 **ස්ථානය:** {info['location']}\n⏰ **හොඳම වේලාව:** {info['best_time']}\n🎫 **ප්‍රවේශ ගාස්තු:** {info['entry_fee']}\n💡 **උපදෙස්:** {info['tips']}"
        else:
            return f"**{info['name']}**\n\n{info['description']}"
    
    def _get_greeting_suggestions(self, language: str) -> List[str]:
        """Get greeting suggestions"""
        suggestions = {
            'en': [
                "What can I visit in Sri Lanka?",
                "Tell me about local food",
                "How do I get around?",
                "Where should I stay?",
                "What's the weather like?"
            ],
            'si': [
                "ශ්‍රී ලංකාවේ මොනාද බලන්න පුළුවන්?",
                "දේශීය ආහාර ගැන කියන්න",
                "කොහොමද යන්න පුළුවන්?",
                "කොහේද ඉන්න පුළුවන්?",
                "කාලගුණය කොහොමද?"
            ],
            'ta': [
                "இலங்கையில் என்ன பார்க்கலாம்?",
                "உள்ளூர் உணவு பற்றி சொல்லுங்கள்",
                "எப்படி சுற்றுவது?",
                "எங்கே தங்குவது?",
                "வானிலை எப்படி இருக்கிறது?"
            ],
            'zh': [
                "斯里兰卡有什么可以参观的？",
                "告诉我当地美食",
                "如何出行？",
                "住在哪里？",
                "天气怎么样？"
            ],
            'fr': [
                "Que puis-je visiter au Sri Lanka?",
                "Parlez-moi de la nourriture locale",
                "Comment se déplacer?",
                "Où loger?",
                "Quel temps fait-il?"
            ]
        }
        return suggestions.get(language, suggestions['en'])
    
    def _get_quick_replies(self, language: str, context: str) -> List[str]:
        """Get quick reply options based on context"""
        quick_replies = {
            'greeting': {
                'en': ["Attractions", "Food", "Transport", "Hotels"],
                'si': ["ආකර්ෂණ", "ආහාර", "ප්‍රවාහනය", "හෝටල්"],
                'ta': ["இடங்கள்", "உணவு", "போக்குவரத்து", "ஹோட்டல்கள்"],
                'zh': ["景点", "美食", "交通", "酒店"],
                'fr': ["Attractions", "Nourriture", "Transport", "Hôtels"]
            }
        }
        return quick_replies.get(context, {}).get(language, [])
    
    def _get_error_response(self, language: str) -> str:
        """Get error response in specified language"""
        responses = {
            'en': "I'm sorry, I encountered an error. Please try again.",
            'si': "සමාවන්න, මට ගැටලුවක් සිදු වුණා. කරුණාකර නැවත උත්සාහ කරන්න.",
            'ta': "மன்னிக்கவும், எனக்கு பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
            'zh': "抱歉，我遇到了错误。请重试。",
            'fr': "Désolé, j'ai rencontré une erreur. Veuillez réessayer."
        }
        return responses.get(language, responses['en'])
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        return self.sessions.get(session_id)
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        session = self.sessions.get(session_id)
        if session:
            return session.get('conversation_history', [])
        return []
    
    def switch_language(self, session_id: str, language: str) -> bool:
        """Switch session language"""
        if session_id in self.sessions and self.language_detector.is_supported_language(language):
            self.sessions[session_id]['language'] = language
            return True
        return False
    
    def switch_guide(self, session_id: str, guide: str) -> bool:
        """Switch virtual tour guide"""
        if session_id in self.sessions and guide in self.tour_guides:
            self.sessions[session_id]['guide'] = guide
            return True
        return False
    
    def get_available_guides(self) -> Dict[str, Any]:
        """Get available tour guides"""
        return self.tour_guides
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages"""
        return self.language_detector.get_supported_languages()
    
    # Additional helper methods for response generation
    def _get_general_attractions_response(self, language: str) -> str:
        """Get general attractions response"""
        responses = {
            'en': "Sri Lanka has amazing attractions! Here are some must-visit places:\n\n🏰 **Sigiriya** - Ancient rock fortress\n🦷 **Kandy** - Temple of the Tooth\n🏰 **Galle Fort** - Colonial architecture\n🐘 **Yala National Park** - Wildlife safari\n🏔️ **Ella** - Scenic hill country",
            'si': "ශ්‍රී ලංකාවේ විස්මයජනක ආකර්ෂණ තියෙනවා! මෙන්න යන්න ඕනේ ස්ථාන:\n\n🏰 **සීගිරිය** - පුරාණ පර්වත කොටුව\n🦷 **කැන්ඩි** - දළදා මාලිගාව\n🏰 **ගාල්ල කොටුව** - යටත් විජිත ගෘහ නිර්මාණ\n🐘 **යාල ජාතික වනෝද්‍යානය** - වන්‍යජීවී සෆාරි\n🏔️ **ඇල්ල** - සුන්දර කඳුකර ප්‍රදේශය"
        }
        return responses.get(language, responses['en'])
    
    def _get_food_response(self, language: str, food_info: Optional[Dict[str, Any]]) -> str:
        """Get food response"""
        if food_info:
            return f"🍛 **{food_info['name']}**\n\n{food_info['description']}\n\n🌶️ **Spice level:** {food_info['spice_level']}\n📍 **Where to try:** {food_info['where_to_try']}"
        
        responses = {
            'en': "Sri Lankan cuisine is amazing! Try rice and curry, hoppers, kottu, and string hoppers. Don't miss the delicious coconut-based curries and spicy sambols!",
            'si': "ශ්‍රී ලාංකික ආහාර විස්මයජනකයි! බත් සහ කරි, ආප්ප, කොත්තු, ඉදිආප්ප පොල් කිරි කරි සහ සම්බෝල් අමතක කරන්න එපා!"
        }
        return responses.get(language, responses['en'])
    
    def _get_transport_response(self, language: str, transport_info: Optional[Dict[str, Any]]) -> str:
        """Get transport response"""
        responses = {
            'en': "🚂 **Trains** - Scenic journeys, book via railway.gov.lk\n🚌 **Buses** - Extensive network, cash payment\n🛺 **Tuk-tuks** - Short distances, negotiate fare\n✈️ **Flights** - Domestic connections available",
            'si': "🚂 **දුම්රිය** - සුන්දර ගමන්, railway.gov.lk හරහා වන්දනාව\n🚌 **බස්** - පුළුල් ජාලය, මුදල් ගෙවීම\n🛺 **ත්‍රීරෝද රථ** - කෙටි දුර, ගාස්තු සාකච්ඡා\n✈️ **ගුවන්** - දේශීය සම්බන්ධතා"
        }
        return responses.get(language, responses['en'])
    
    def _get_accommodation_response(self, language: str) -> str:
        """Get accommodation response"""
        responses = {
            'en': "🏨 Sri Lanka offers various accommodation options:\n\n🏖️ **Beach resorts** - Bentota, Hikkaduwa\n🏔️ **Hill country hotels** - Kandy, Nuwara Eliya\n🏛️ **Boutique hotels** - Galle Fort, Colombo\n🏠 **Guesthouses** - Budget-friendly options\n🐘 **Eco lodges** - Near national parks",
            'si': "🏨 ශ්‍රී ලංකාවේ විවිධ නවාතැන් විකල්ප:\n\n🏖️ **වෙරළ නිකේතන** - බෙන්තොට, හික්කඩුව\n🏔️ **කඳුකර හෝටල්** - කැන්ඩි, නුවරඑළිය\n🏛️ **බුටික් හෝටල්** - ගාල්ල කොටුව, කොළඹ\n🏠 **ගෘහ නවාතැන්** - අඩු මිල විකල්ප\n🐘 **පරිසර නවාතැන්** - ජාතික වනෝද්‍යාන අසල"
        }
        return responses.get(language, responses['en'])
    
    def _get_weather_response(self, language: str) -> str:
        """Get weather response"""
        responses = {
            'en': "🌤️ Sri Lanka has a tropical climate:\n\n☀️ **Dry season** - December to April (West/South coast)\n🌧️ **Monsoon season** - May to September (Southwest), October to March (Northeast)\n🌡️ **Temperature** - 26-30°C year-round\n🏖️ **Best beach weather** - November to April",
            'si': "🌤️ ශ්‍රී ලංකාවේ නිවර්තන දේශගුණයක්:\n\n☀️ **වියලි කාලය** - දෙසැම්බර් සිට අප්‍රේල් (බටහිර/දකුණු වෙරළ)\n🌧️ **මෝසම් කාලය** - මැයි සිට සැප්තැම්බර් (නිරිතදිග), ඔක්තෝබර් සිට මාර්තු (ඊසානදිග)\n🌡️ **උෂ්ණත්වය** - වසර පුරා 26-30°C\n🏖️ **හොඳම වෙරළ කාලගුණය** - නොවැම්බර් සිට අප්‍රේල්"
        }
        return responses.get(language, responses['en'])
    
    def _get_help_response(self, language: str) -> str:
        """Get help response"""
        responses = {
            'en': "I'm here to help you explore Sri Lanka! I can assist with:\n\n🏛️ **Attractions** - Historical sites, temples, nature\n🍛 **Food** - Local cuisine and where to try it\n🚂 **Transport** - Trains, buses, taxis\n🏨 **Accommodation** - Hotels and guesthouses\n🌤️ **Weather** - Climate and best travel times\n🎭 **Culture** - Etiquette and festivals\n\nJust ask me anything about Sri Lanka!",
            'si': "ශ්‍රී ලංකාව ගවේෂණය කිරීමට මම ඔබට උදව් කරන්නම්! මට උදව් කරන්න පුළුවන්:\n\n🏛️ **ආකර්ෂණ** - ඓතිහාසික ස්ථාන, දේවාල, ස්වභාවික\n🍛 **ආහාර** - දේශීය ආහාර සහ කොහේ අත්දකින්න\n🚂 **ප්‍රවාහනය** - දුම්රිය, බස්, ටැක්සි\n🏨 **නවාතැන්** - හෝටල් සහ ගෘහ නවාතැන්\n🌤️ **කාලගුණය** - දේශගුණය සහ හොඳම ගමන් කාල\n🎭 **සංස්කෘතිය** - ආචාර ධර්ම සහ උත්සව\n\nශ්‍රී ලංකාව ගැන ඕනෑම දෙයක් අහන්න!"
        }
        return responses.get(language, responses['en'])
    
    def _get_goodbye_response(self, language: str, guide: str) -> str:
        """Get goodbye response"""
        responses = {
            'en': f"Thank you for chatting with me! Have a wonderful time exploring Sri Lanka! 🇱🇰✨\n\n- {self.tour_guides[guide]['name']}",
            'si': f"මා සමඟ කතා කිරීමට ස්තූතියි! ශ්‍රී ලංකාව ගවේෂණය කරන්න ලස්සන කාලයක් ගත කරන්න! 🇱🇰✨\n\n- {self.tour_guides[guide]['name']}",
            'ta': f"என்னுடன் பேசியதற்கு நன்றி! இலங்கையை ஆராய்வதில் அற்புதமான நேரத்தைப் பெறுங்கள்! 🇱🇰✨\n\n- {self.tour_guides[guide]['name']}",
            'zh': f"谢谢您与我聊天！祝您在斯里兰卡探索愉快！🇱🇰✨\n\n- {self.tour_guides[guide]['name']}",
            'fr': f"Merci d'avoir discuté avec moi! Passez un merveilleux moment à explorer le Sri Lanka! 🇱🇰✨\n\n- {self.tour_guides[guide]['name']}"
        }
        return responses.get(language, responses['en'])
    
    def _get_unknown_response(self, language: str) -> str:
        """Get response for unknown intent"""
        responses = {
            'en': "I'm not sure I understand that completely. Could you tell me more about what you'd like to know about Sri Lanka? I can help with attractions, food, transport, accommodation, and more!",
            'si': "මට ඒක සම්පූර්ණයෙන්ම තේරුම් වෙන්නේ නෑ. ශ්‍රී ලංකාව ගැන ඔබ දැන ගන්න කැමති දේ ගැන තව කියන්න පුළුවන්ද? මට ආකර්ෂණ, ආහාර, ප්‍රවාහනය, නවාතැන් සහ තවත් දේවල් ගැන උදව් කරන්න පුළුවන්!",
            'ta': "அது எனக்கு முழுமையாக புரியவில்லை. இலங்கையைப் பற்றி நீங்கள் தெரிந்து கொள்ள விரும்புவதைப் பற்றி மேலும் சொல்ல முடியுமா? நான் இடங்கள், உணவு, போக்குவரத்து, தங்குமிடம் மற்றும் பலவற்றில் உதவ முடியும்!",
            'zh': "我不太理解。您能告诉我更多关于您想了解斯里兰卡什么的信息吗？我可以帮助您了解景点、美食、交通、住宿等等！",
            'fr': "Je ne comprends pas complètement. Pourriez-vous me dire ce que vous aimeriez savoir sur le Sri Lanka? Je peux vous aider avec les attractions, la nourriture, le transport, l'hébergement et plus encore!"
        }
        return responses.get(language, responses['en'])
    
    def _get_attraction_suggestions(self, language: str) -> List[str]:
        """Get attraction suggestions"""
        return ["Sigiriya", "Kandy Temple", "Galle Fort", "Yala Safari", "Ella Nine Arch Bridge"]
    
    def _get_food_suggestions(self, language: str) -> List[str]:
        """Get food suggestions"""
        return ["Rice and Curry", "Hoppers", "Kottu Roti", "String Hoppers", "Fish Curry"]
    
    def _get_transport_suggestions(self, language: str) -> List[str]:
        """Get transport suggestions"""
        return ["Train to Ella", "Bus routes", "Tuk-tuk fares", "Airport transfers", "Taxi booking"]
    
    def _get_accommodation_suggestions(self, language: str) -> List[str]:
        """Get accommodation suggestions"""
        return ["Beach resorts", "Hill country hotels", "Budget guesthouses", "Boutique hotels", "Eco lodges"]
    
    def _get_weather_suggestions(self, language: str) -> List[str]:
        """Get weather suggestions"""
        return ["Best travel months", "Monsoon seasons", "Beach weather", "Hill country climate", "What to pack"]
    
    def _get_help_suggestions(self, language: str) -> List[str]:
        """Get help suggestions"""
        return ["Popular attractions", "Local food guide", "Transport options", "Cultural etiquette", "Emergency contacts"]
    
    def _get_general_suggestions(self, language: str) -> List[str]:
        """Get general suggestions"""
        return self._get_greeting_suggestions(language)
    
    def _format_search_results(self, results: List[Dict[str, Any]], language: str) -> str:
        """Format search results"""
        if not results:
            return self._get_unknown_response(language)
        
        response_parts = ["Here's what I found:"]
        
        for result in results[:3]:  # Limit to 3 results
            info = result['info']
            if result['type'] == 'attraction':
                response_parts.append(f"📍 **{info['name']}** - {info['description']}")
            elif result['type'] == 'food':
                response_parts.append(f"🍛 **{info['name']}** - {info['description']}")
            elif result['type'] == 'transport':
                response_parts.append(f"🚂 **Transportation** - {info['description']}")
        
        return '\n\n'.join(response_parts)