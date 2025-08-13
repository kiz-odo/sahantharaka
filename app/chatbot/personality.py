"""
Tour Guide Personality Component

Adds character and personality to the chatbot responses, making it feel
like a friendly local tour guide named "Saru" or "Anjali".
"""

import random
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TourGuidePersonality:
    """
    Personality-driven tour guide that adds character and contextualization
    to chatbot responses.
    """
    
    def __init__(self, guide_name: str = None):
        """
        Initialize the tour guide personality.
        
        Args:
            guide_name: Name of the tour guide ('Saru' or 'Anjali')
        """
        self.guide_name = guide_name or random.choice(['Saru', 'Anjali'])
        self.personality_traits = self._initialize_personality_traits()
        self.conversation_style = self._initialize_conversation_style()
        self.cultural_insights = self._initialize_cultural_insights()
        
        logger.info(f"Tour Guide Personality '{self.guide_name}' initialized successfully")
    
    def _initialize_personality_traits(self) -> Dict:
        """Initialize personality traits for the tour guide."""
        return {
            'friendly': True,
            'knowledgeable': True,
            'enthusiastic': True,
            'helpful': True,
            'cultural_expert': True,
            'local_insider': True,
            'patient': True,
            'humorous': True
        }
    
    def _initialize_conversation_style(self) -> Dict:
        """Initialize conversation style patterns."""
        return {
            'greetings': {
                'en': [
                    f"Hi there! I'm {self.guide_name}, your friendly Sri Lanka tour guide!",
                    f"Hello! {self.guide_name} here, ready to show you the wonders of Sri Lanka!",
                    f"Ayubowan! I'm {self.guide_name}, and I'm excited to help you explore!"
                ],
                'si': [
                    f"ආයුබෝවන්! මම {self.guide_name}, ඔබේ මිතුරා ශ්‍රී ලංකා සංචාරක මඟපෙන්වීම් කරන්නෙමි!",
                    f"ආයුබෝවන්! මෙතැන {self.guide_name}, ශ්‍රී ලංකාවේ ආශ්චර්‍ය පෙන්වීමට සූදානම්!"
                ],
                'ta': [
                    f"வணக்கம்! நான் {self.guide_name}, உங்கள் நட்பு இலங்கை சுற்றுலா வழிகாட்டி!",
                    f"வணக்கம்! இங்கே {self.guide_name}, இலங்கையின் அதிசயங்களைக் காட்ட தயாராக உள்ளேன்!"
                ]
            },
            'enthusiasm': {
                'en': [
                    "Oh, that's a fantastic choice!",
                    "Excellent question! Let me tell you all about it.",
                    "I'm so excited you asked about that!",
                    "That's one of my favorite topics!"
                ],
                'si': [
                    "ඔව්, ඒක නියම තේරීමක්!",
                    "පුදුම ප්‍රශ්නයක්! මම ඒ ගැන සියල්ලම කියන්නම්.",
                    "ඔබ ඒ ගැන ඇසූ නිසා මට ගොඩක් සතුටක්!"
                ],
                'ta': [
                    "ஆம், அது ஒரு அருமையான தேர்வு!",
                    "சிறந்த கேள்வி! அதைப் பற்றி எல்லாம் சொல்கிறேன்.",
                    "நீங்கள் அதைப் பற்றி கேட்டதில் நான் மிகவும் மகிழ்ச்சியடைகிறேன்!"
                ]
            },
            'personal_touch': {
                'en': [
                    "I remember when I first visited there...",
                    "Let me share a little secret with you...",
                    "From my experience as a local guide...",
                    "I always recommend this to my friends..."
                ],
                'si': [
                    "මම මුලින්ම එතැනට ගිය විට මතකයි...",
                    "මම ඔබට කුඩා රහසක් කියන්නම්...",
                    "ස්ථානීය මඟපෙන්වීම් කරන්නෙක් ලෙස මගේ අත්දැකීමෙන්..."
                ],
                'ta': [
                    "நான் முதலில் அங்கு சென்றபோது நினைவிருக்கிறது...",
                    "நான் உங்களுடன் ஒரு சிறிய இரகசியத்தை பகிர்கிறேன்...",
                    "உள்ளூர் வழிகாட்டியாக எனது அனுபவத்திலிருந்து..."
                ]
            },
            'encouragement': {
                'en': [
                    "You're going to love it!",
                    "Trust me, you won't be disappointed!",
                    "This is definitely worth your time!",
                    "I guarantee you'll have an amazing experience!"
                ],
                'si': [
                    "ඔබට ඒක ගොඩක් ආස වෙයි!",
                    "මාව විශ්වාස කරන්න, ඔබට කලකිරීමක් නොවේවි!",
                    "මෙය නිසැකවම ඔබේ කාලය වටිනවා!"
                ],
                'ta': [
                    "நீங்கள் அதை விரும்புவீர்கள்!",
                    "என்னை நம்புங்கள், நீங்கள் ஏமாற்றமடைய மாட்டீர்கள்!",
                    "இது நிச்சயமாக உங்கள் நேரத்திற்கு மதிப்புள்ளது!"
                ]
            },
            'cultural_connection': {
                'en': [
                    "This is such an important part of our culture...",
                    "You know, this tradition goes back centuries...",
                    "This really shows the heart of Sri Lanka...",
                    "I'm proud to share this with you..."
                ],
                'si': [
                    "මෙය අපේ සංස්කෘතියේ ඉතා වැදගත් කොටසක්...",
                    "ඔබ දන්නවාද, මෙම සම්ප්‍රදාය සියවස් ගණනක් පෙරට..."
                ],
                'ta': [
                    "இது நமது கலாச்சாரத்தின் மிகவும் முக்கியமான பகுதி...",
                    "உங்களுக்குத் தெரியுமா, இந்த பாரம்பரியம் நூற்றாண்டுகளுக்கு முன்பு..."
                ]
            }
        }
    
    def _initialize_cultural_insights(self) -> Dict:
        """Initialize cultural insights and local knowledge."""
        return {
            'local_tips': {
                'en': [
                    "Pro tip: Visit early morning to avoid crowds!",
                    "Local secret: Try the street food near the temple!",
                    "Insider tip: Ask for the 'local price' not tourist price!",
                    "My recommendation: Go during the off-season for better deals!"
                ],
                'si': [
                    "වෘත්තීය උපදෙස්: බහුල ජනයා වළක්වා ගැනීමට උදෑසන ගොස් බලන්න!",
                    "ස්ථානීය රහස: දේවාලය අසල තිබෙන වීදි ආහාර උත්සාහ කරන්න!"
                ],
                'ta': [
                    "தொழில் குறிப்பு: கூட்டத்தைத் தவிர்க்க காலையில் செல்லுங்கள்!",
                    "உள்ளூர் இரகசியம்: கோவிலுக்கு அருகே உள்ள தெரு உணவை முயற்சிக்கவும்!"
                ]
            },
            'seasonal_advice': {
                'en': [
                    "Perfect timing! This is the best season to visit.",
                    "You've picked a great time! The weather is ideal now.",
                    "Consider visiting during the festival season for a unique experience!",
                    "This time of year offers the most beautiful views!"
                ]
            },
            'personal_experiences': {
                'en': [
                    "I took my family there last month and they loved it!",
                    "This is where I had my first cup of Ceylon tea!",
                    "I've been guiding tours here for years and never get tired of it!",
                    "This place holds a special place in my heart!"
                ]
            }
        }
    
    def personalize_response(self, base_response: str, intent: str, 
                           language: str, session: Dict) -> str:
        """
        Personalize a base response with personality elements.
        
        Args:
            base_response: Base response from knowledge base
            intent: Detected intent
            language: Language code
            session: User session information
            
        Returns:
            Personalized response with personality elements
        """
        try:
            # Start with base response
            personalized_response = base_response
            
            # Add personality elements based on intent and context
            if intent == 'greeting':
                personalized_response = self._add_greeting_personality(base_response, language)
            elif intent in ['attraction_info', 'food_info', 'culture_info']:
                personalized_response = self._add_enthusiasm_personality(base_response, language)
            elif intent in ['transport_info', 'accommodation_info']:
                personalized_response = self._add_helpful_personality(base_response, language)
            
            # Add cultural insights if appropriate
            if intent in ['attraction_info', 'food_info', 'culture_info']:
                personalized_response = self._add_cultural_insight(personalized_response, language)
            
            # Add personal touch based on conversation history
            if session.get('conversation_history'):
                personalized_response = self._add_personal_touch(personalized_response, language, session)
            
            # Add encouragement for positive interactions
            if intent != 'goodbye':
                personalized_response = self._add_encouragement(personalized_response, language)
            
            return personalized_response
            
        except Exception as e:
            logger.error(f"Error personalizing response: {str(e)}")
            return base_response
    
    def _add_greeting_personality(self, response: str, language: str) -> str:
        """Add greeting personality to the response."""
        if language in self.conversation_style['greetings']:
            greeting = random.choice(self.conversation_style['greetings'][language])
            return f"{greeting} {response}"
        return response
    
    def _add_enthusiasm_personality(self, response: str, language: str) -> str:
        """Add enthusiasm to the response."""
        if language in self.conversation_style['enthusiasm']:
            enthusiasm = random.choice(self.conversation_style['enthusiasm'][language])
            return f"{enthusiasm} {response}"
        return response
    
    def _add_helpful_personality(self, response: str, language: str) -> str:
        """Add helpful personality to the response."""
        # Add helpful tips or suggestions
        if language == 'en':
            helpful_tips = [
                "Let me help you with that! ",
                "I'm here to make your trip easier! ",
                "Here's what you need to know: ",
                "Let me give you the inside scoop: "
            ]
            tip = random.choice(helpful_tips)
            return f"{tip}{response}"
        return response
    
    def _add_cultural_insight(self, response: str, language: str) -> str:
        """Add cultural insights to the response."""
        if language in self.cultural_insights['local_tips']:
            insight = random.choice(self.cultural_insights['local_tips'][language])
            return f"{response}\n\n💡 {insight}"
        return response
    
    def _add_personal_touch(self, response: str, language: str, session: Dict) -> str:
        """Add personal touch based on conversation history."""
        if language in self.conversation_style['personal_touch']:
            # Only add personal touch occasionally to avoid repetition
            if random.random() < 0.3:  # 30% chance
                personal = random.choice(self.conversation_style['personal_touch'][language])
                return f"{response}\n\n{personal}"
        return response
    
    def _add_encouragement(self, response: str, language: str) -> str:
        """Add encouragement to the response."""
        if language in self.conversation_style['encouragement']:
            # Add encouragement occasionally
            if random.random() < 0.4:  # 40% chance
                encouragement = random.choice(self.conversation_style['encouragement'][language])
                return f"{response}\n\n✨ {encouragement}"
        return response
    
    def get_guide_introduction(self, language: str) -> str:
        """Get a personalized introduction from the tour guide."""
        introductions = {
            'en': [
                f"Hi! I'm {self.guide_name}, your personal Sri Lanka tour guide! I've been exploring this beautiful island for years and I can't wait to share all its secrets with you. Whether you're interested in ancient temples, pristine beaches, or delicious local cuisine, I'm here to make your journey unforgettable!",
                f"Welcome! I'm {self.guide_name}, and I'm absolutely passionate about Sri Lanka! From the misty mountains of Kandy to the golden beaches of the south, I know every hidden gem and local secret. Let's make your trip extraordinary together!"
            ],
            'si': [
                f"ආයුබෝවන්! මම {self.guide_name}, ඔබේ පුද්ගලික ශ්‍රී ලංකා සංචාරක මඟපෙන්වීම් කරන්නෙමි! මම මෙම සුන්දර දිවයින ගවේෂණය කර ඇති වසර ගණනක් ඇත, එහි සියලුම රහස් ඔබ සමඟ බෙදා ගැනීමට මට බලාපොරොත්තු වෙමි.",
                f"සාදරයෙන් පිළිගනිමු! මම {self.guide_name}, ශ්‍රී ලංකාව ගැන මට අවශ්‍යයි! මහනුවරේ මීදුම් කඳුවල සිට දකුණේ රන්වන් වෙරළ දක්වා, මම සෑම සඟවා ඇති මැණික් සහ ස්ථානීය රහස් දන්නවා."
            ],
            'ta': [
                f"வணக்கம்! நான் {self.guide_name}, உங்கள் தனிப்பட்ட இலங்கை சுற்றுலா வழிகாட்டி! நான் இந்த அழகான தீவை ஆண்டுகள் ஆராய்ந்துள்ளேன், அதன் அனைத்து இரகசியங்களையும் உங்களுடன் பகிர்ந்து கொள்ள ஆவலாக உள்ளேன்.",
                f"வரவேற்கிறோம்! நான் {self.guide_name}, இலங்கையைப் பற்றி முற்றிலும் ஆர்வமாக உள்ளேன்! கண்டியின் மூடுபனி மலைகளிலிருந்து தெற்கின் தங்க வெளிகள்வரை, நான் ஒவ்வொரு மறைக்கப்பட்ட மாணிக்கம் மற்றும் உள்ளூர் இரகசியத்தையும் அறிவேன்."
            ]
        }
        
        if language in introductions:
            return random.choice(introductions[language])
        else:
            return random.choice(introductions['en'])
    
    def get_farewell_message(self, language: str, session: Dict) -> str:
        """Get a personalized farewell message."""
        farewells = {
            'en': [
                f"Thank you for letting me be your guide today! I hope I've helped you discover the magic of Sri Lanka. Remember, {self.guide_name} is always here when you need travel advice. Have a wonderful journey, and come back soon! Ayubowan! 🙏",
                f"It's been such a pleasure guiding you through Sri Lanka's wonders! I hope you've learned something new and exciting. Safe travels, and don't forget to share your amazing experiences with others. Until next time! Ayubowan! ✨"
            ],
            'si': [
                f"අද මම ඔබේ මඟපෙන්වීම් කිරීමට ඉඩ ලබා දුන් ඔබට ස්තූතියි! මම ශ්‍රී ලංකාවේ මායාව සොයා ගැනීමට උදව් කළා යැයි බලාපොරොත්තු වෙමි. මතක තබා ගන්න, {self.guide_name} සෑම විටම ඔබට ගමන් උපදෙස් අවශ්‍ය විට මෙහි සිටී.",
                f"ශ්‍රී ලංකාවේ ආශ්චර්‍ය ඔබට මඟපෙන්වීම ඉතා සතුටක්! ඔබ යමක් අලුත් සහ ගල්වෙන දේ ඉගෙන ගත්තා යැයි බලාපොරොත්තු වෙමි."
            ],
            'ta': [
                f"இன்று நான் உங்கள் வழிகாட்டியாக இருப்பதற்கு நன்றி! நான் இலங்கையின் மாயத்தை கண்டுபிடிக்க உதவியுள்ளேன் என்று நம்புகிறேன். நினைவில் கொள்ளுங்கள், {self.guide_name} எப்போதும் உங்களுக்கு பயண ஆலோசனை தேவைப்படும்போது இங்கே இருக்கிறார்.",
                f"இலங்கையின் அதிசயங்களில் உங்களை வழிநடத்துவது மிகவும் மகிழ்ச்சியாக இருந்தது! நீங்கள் ஏதாவது புதிய மற்றும் உற்சாகமானதைக் கற்றுக்கொண்டீர்கள் என்று நம்புகிறேன்."
            ]
        }
        
        if language in farewells:
            return random.choice(farewells[language])
        else:
            return random.choice(farewells['en'])
    
    def get_guide_name(self) -> str:
        """Get the current guide name."""
        return self.guide_name
    
    def change_guide(self, new_name: str):
        """Change the tour guide personality."""
        if new_name in ['Saru', 'Anjali']:
            self.guide_name = new_name
            logger.info(f"Tour guide changed to {new_name}")
        else:
            logger.warning(f"Invalid guide name: {new_name}. Must be 'Saru' or 'Anjali'")
    
    def get_personality_summary(self) -> Dict:
        """Get a summary of the current personality traits."""
        return {
            'guide_name': self.guide_name,
            'personality_traits': self.personality_traits.copy(),
            'conversation_style': list(self.conversation_style.keys()),
            'cultural_insights': list(self.cultural_insights.keys())
        }