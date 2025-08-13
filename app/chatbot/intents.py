"""
Intent Detection Component

Detects user intentions from messages in Sinhala, Tamil, and English
using pattern matching and keyword analysis.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class IntentHandler:
    """
    Handles intent detection for tourism-related queries in multiple languages.
    """
    
    def __init__(self):
        """Initialize the intent handler."""
        self.intent_patterns = self._initialize_intent_patterns()
        self.entity_patterns = self._initialize_entity_patterns()
        logger.info("Intent Handler initialized successfully")
    
    def _initialize_intent_patterns(self) -> Dict:
        """Initialize intent patterns for different languages."""
        return {
            'greeting': {
                'en': [
                    r'\b(hi|hello|hey|good morning|good afternoon|good evening|ayubowan)\b',
                    r'\b(welcome|greetings)\b',
                    r'\b(start|begin|help)\b'
                ],
                'si': [
                    r'\b(ආයුබෝවන්|ආයුබෝවන්|ස්තූතියි|ආයුබෝවන්|ආයුබෝවන්)\b',
                    r'\b(ආයුබෝවන්|ආයුබෝවන්|ආයුබෝවන්)\b',
                    r'\b(ආයුබෝවන්|ආයුබෝවන්|ආයුබෝවන්)\b'
                ],
                'ta': [
                    r'\b(வணக்கம்|வணக்கம்|வணக்கம்|வணக்கம்|வணக்கம்)\b',
                    r'\b(வணக்கம்|வணக்கம்|வணக்கம்)\b',
                    r'\b(வணக்கம்|வணக்கம்|வணக்கம்)\b'
                ]
            },
            'goodbye': {
                'en': [
                    r'\b(bye|goodbye|see you|farewell|thank you|thanks)\b',
                    r'\b(end|stop|quit|exit)\b'
                ],
                'si': [
                    r'\b(ආයුබෝවන්|ස්තූතියි|ආයුබෝවන්|ආයුබෝවන්)\b',
                    r'\b(ආයුබෝවන්|ආයුබෝවන්|ආයුබෝවන්)\b'
                ],
                'ta': [
                    r'\b(வணக்கம்|நன்றி|வணக்கம்|வணக்கம்)\b',
                    r'\b(வணக்கம்|வணக்கம்|வணக்கம்)\b'
                ]
            },
            'attraction_info': {
                'en': [
                    r'\b(attraction|place|visit|see|tour|sight|landmark)\b',
                    r'\b(sigiriya|kandy|galle|fort|temple|palace|garden)\b',
                    r'\b(what to see|where to go|popular places|must see)\b',
                    r'\b(historical|ancient|cultural|heritage)\b'
                ],
                'si': [
                    r'\b(සංචාරක|ස්ථාන|ගොස්|බලන්න|සංචාර|දැක්ම|සලකුණ)\b',
                    r'\b(සීගිරිය|මහනුවර|ගාල්ල|කොටුව|දේවාලය|මාලිගාව|උද්‍යාන)\b',
                    r'\b(කුමක් බලන්නද|කොහෙද යන්නද|ජනප්‍රිය ස්ථාන|බලාගත යුතු)\b'
                ],
                'ta': [
                    r'\b(சுற்றுலா|இடம்|செல்ல|பார்க்க|சுற்றுலா|பார்வை|அடையாளம்)\b',
                    r'\b(சிகிரியா|கண்டி|காலி|கோட்டை|கோவில்|அரண்மனை|பூங்கா)\b',
                    r'\b(என்ன பார்க்க|எங்கே செல்ல|பிரபலமான இடங்கள்|பார்க்க வேண்டியவை)\b'
                ]
            },
            'food_info': {
                'en': [
                    r'\b(food|cuisine|dish|meal|restaurant|eat|dining)\b',
                    r'\b(rice|curry|hoppers|kottu|roti|spicy|traditional)\b',
                    r'\b(what to eat|local food|sri lankan food|cuisine)\b',
                    r'\b(breakfast|lunch|dinner|snack)\b'
                ],
                'si': [
                    r'\b(ආහාර|පාන|විශේෂ|ආහාර|අවන්හල|කන්න|ආහාර)\b',
                    r'\b(බත්|කරවල|ආප්ප|කොට්ටු|රොටි|මසාල|සම්ප්‍රදායික)\b',
                    r'\b(කුමක් කන්නද|ස්ථානීය ආහාර|ශ්‍රී ලාංකීය ආහාර)\b'
                ],
                'ta': [
                    r'\b(உணவு|சமையல்|வகை|உணவு|உணவகம்|சாப்பிட|உணவு)\b',
                    r'\b(அரிசி|குழம்பு|அப்பம்|கொட்டு|ரொட்டி|மசாலா|பாரம்பரிய)\b',
                    r'\b(என்ன சாப்பிட|உள்ளூர் உணவு|இலங்கை உணவு)\b'
                ]
            },
            'culture_info': {
                'en': [
                    r'\b(culture|custom|tradition|etiquette|greeting|festival)\b',
                    r'\b(temple|buddhist|religion|spiritual|ceremony|ritual)\b',
                    r'\b(how to greet|what to wear|behavior|manners)\b',
                    r'\b(sinhala|tamil|language|local customs)\b'
                ],
                'si': [
                    r'\b(සංස්කෘතිය|පුරුද්ද|සම්ප්‍රදාය|ආචාර|ආයුබෝවන්|උත්සව)\b',
                    r'\b(දේවාලය|බෞද්ධ|ආගම|ආධ්‍යාත්මික|විධිය|චාරිත්‍ර)\b',
                    r'\b(කෙසේ ආයුබෝවන් කරන්නද|කුමක් ඇඳීමටද|හැසිරීම|ආචාර)\b'
                ],
                'ta': [
                    r'\b(கலாச்சாரம்|பழக்கம்|பாரம்பரியம்|நடத்தை|வணக்கம்|திருவிழா)\b',
                    r'\b(கோவில்|புத்த|மதம்|ஆன்மீக|சடங்கு|சடங்கு)\b',
                    r'\b(எப்படி வணங்க|என்ன அணிய|நடத்தை|நடத்தை)\b'
                ]
            },
            'transport_info': {
                'en': [
                    r'\b(transport|transportation|travel|get to|how to reach)\b',
                    r'\b(bus|train|tuk tuk|taxi|car|rent|drive)\b',
                    r'\b(from|to|route|schedule|fare|cost|price)\b',
                    r'\b(airport|station|terminal|departure|arrival)\b'
                ],
                'si': [
                    r'\b(ප්‍රවාහන|ප්‍රවාහන|ගමන්|ලබා ගන්න|කෙසේ ළඟා වන්නද)\b',
                    r'\b(බස්|දුම්රිය|ටුක් ටුක්|ටැක්සි|මෝටර් රථ|කුලිය|මෝටර් රථ)\b',
                    r'\b(සිට|වෙත|මාර්ගය|කාලසටහන|වාරික|පිරිවැය|මිල)\b'
                ],
                'ta': [
                    r'\b(போக்குவரத்து|போக்குவரத்து|பயணம்|கிடைக்க|எப்படி அடைய)\b',
                    r'\b(பஸ்|ரயில்|டக் டக்|டாக்சி|கார்|வாடகை|ஓட்ட)\b',
                    r'\b(இருந்து|வரை|வழி|அட்டவணை|கட்டணம்|செலவு|விலை)\b'
                ]
            },
            'accommodation_info': {
                'en': [
                    r'\b(accommodation|hotel|guesthouse|homestay|stay|sleep)\b',
                    r'\b(room|booking|reservation|check in|check out)\b',
                    r'\b(where to stay|place to sleep|lodging|hostel)\b',
                    r'\b(price|cost|budget|luxury|cheap|expensive)\b'
                ],
                'si': [
                    r'\b(නවාතැන්|හෝටල්|ගෙවල්|නිවසේ රැඳී සිටීම|රැඳී සිටීම|නින්ද)\b',
                    r'\b(කාමරය|වෙන් කිරීම|වෙන් කිරීම|පිවිසීම|පිටවීම)\b',
                    r'\b(කොහෙද රැඳී සිටීමටද|නින්දට තැන|නවාතැන්|බඩුගෙවල්)\b'
                ],
                'ta': [
                    r'\b(வசிப்பிடம்|ஹோட்டல்|விருந்தோம்பல் வீடு|வீட்டில் தங்குதல்|தங்க|தூங்க)\b',
                    r'\b(அறை|முன்பதிவு|முன்பதிவு|செக் இன்|செக் அவுட்)\b',
                    r'\b(எங்கே தங்க|தூங்க இடம்|வசிப்பிடம்|விடுதி)\b'
                ]
            }
        }
    
    def _initialize_entity_patterns(self) -> Dict:
        """Initialize entity extraction patterns."""
        return {
            'attraction': {
                'en': [
                    r'\b(sigiriya|kandy|galle fort|temple of the tooth|botanical gardens)\b',
                    r'\b(ancient city|fort|palace|garden|museum)\b'
                ],
                'si': [
                    r'\b(සීගිරිය|මහනුවර|ගාල්ල කොටුව|ශ්‍රී දන්ත ධාතුන් වහන්සේගේ දේවාලය|උද්‍යාන)\b'
                ],
                'ta': [
                    r'\b(சிகிரியா|கண்டி|காலி கோட்டை|தந்தம் கோவில்|பூங்கா)\b'
                ]
            },
            'food': {
                'en': [
                    r'\b(rice and curry|hoppers|kottu roti|string hoppers|lamprais)\b',
                    r'\b(curry|dhal|chutney|sambol|pickle)\b'
                ],
                'si': [
                    r'\b(බත් සහ කරවල|ආප්ප|කොට්ටු රොටි|ඉඳි ආප්ප|ලම්ප්රයිස්)\b'
                ],
                'ta': [
                    r'\b(சோறு மற்றும் குழம்பு|அப்பம்|கொட்டு ரொட்டி|இடை அப்பம்|லம்பிரைஸ்)\b'
                ]
            },
            'culture_topic': {
                'en': [
                    r'\b(greeting|etiquette|festival|custom|tradition)\b',
                    r'\b(temple|buddhist|religion|ceremony|ritual)\b'
                ],
                'si': [
                    r'\b(ආයුබෝවන්|ආචාර|උත්සව|පුරුද්ද|සම්ප්‍රදාය)\b'
                ],
                'ta': [
                    r'\b(வணக்கம்|நடத்தை|திருவிழா|பழக்கம்|பாரம்பரியம்)\b'
                ]
            },
            'transport_type': {
                'en': [
                    r'\b(bus|train|tuk tuk|taxi|car|scooter)\b',
                    r'\b(public transport|private transport|rental)\b'
                ],
                'si': [
                    r'\b(බස්|දුම්රිය|ටුක් ටුක්|ටැක්සි|මෝටර් රථ|ස්කූටර්)\b'
                ],
                'ta': [
                    r'\b(பஸ்|ரயில்|டக் டக்|டாக்சி|கார்|ஸ்கூட்டர்)\b'
                ]
            },
            'accommodation_type': {
                'en': [
                    r'\b(hotel|guesthouse|homestay|hostel|resort)\b',
                    r'\b(budget|luxury|mid-range|boutique|eco-friendly)\b'
                ],
                'si': [
                    r'\b(හෝටල්|ගෙවල්|නිවසේ රැඳී සිටීම|බඩුගෙවල්|විවේකාගාර)\b'
                ],
                'ta': [
                    r'\b(ஹோட்டல்|விருந்தோம்பல் வீடு|வீட்டில் தங்குதல்|விடுதி|விடுமுறை)\b'
                ]
            }
        }
    
    def detect_intent(self, message: str, language: str) -> Dict:
        """
        Detect intent and extract entities from user message.
        
        Args:
            message: User's message text
            language: Language code ('en', 'si', 'ta')
            
        Returns:
            Dictionary containing intent, confidence, and entities
        """
        try:
            message_lower = message.lower().strip()
            
            # Detect intent
            intent, confidence = self._detect_intent(message_lower, language)
            
            # Extract entities
            entities = self._extract_entities(message_lower, language)
            
            return {
                'intent': intent,
                'confidence': confidence,
                'entities': entities,
                'original_message': message,
                'detected_language': language
            }
            
        except Exception as e:
            logger.error(f"Error detecting intent: {str(e)}")
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'entities': [],
                'original_message': message,
                'detected_language': language
            }
    
    def _detect_intent(self, message: str, language: str) -> Tuple[str, float]:
        """
        Detect the primary intent from the message.
        
        Args:
            message: Lowercase message text
            language: Language code
            
        Returns:
            Tuple of (intent, confidence)
        """
        intent_scores = defaultdict(float)
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            if language in patterns:
                for pattern in patterns[language]:
                    matches = re.findall(pattern, message, re.IGNORECASE)
                    if matches:
                        # Score based on number of matches and pattern complexity
                        score = len(matches) * 0.3
                        if len(pattern) > 20:  # Longer patterns get higher weight
                            score += 0.2
                        intent_scores[intent] += score
        
        # If no patterns matched, try fallback detection
        if not intent_scores:
            return self._fallback_intent_detection(message, language)
        
        # Return intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = min(intent_scores[best_intent], 1.0)  # Cap at 1.0
        
        return best_intent, confidence
    
    def _fallback_intent_detection(self, message: str, language: str) -> Tuple[str, float]:
        """
        Fallback intent detection using simple keyword matching.
        
        Args:
            message: Lowercase message text
            language: Language code
            
        Returns:
            Tuple of (intent, confidence)
        """
        # Simple keyword-based fallback
        keywords = {
            'greeting': ['hello', 'hi', 'hey', 'welcome', 'start', 'begin'],
            'attraction_info': ['place', 'visit', 'see', 'go', 'attraction', 'tourist'],
            'food_info': ['food', 'eat', 'restaurant', 'cuisine', 'dish', 'meal'],
            'culture_info': ['culture', 'custom', 'tradition', 'etiquette', 'greeting'],
            'transport_info': ['transport', 'travel', 'bus', 'train', 'car', 'how to'],
            'accommodation_info': ['hotel', 'stay', 'sleep', 'room', 'accommodation']
        }
        
        for intent, intent_keywords in keywords.items():
            for keyword in intent_keywords:
                if keyword in message:
                    return intent, 0.5  # Lower confidence for fallback
        
        return 'unknown', 0.0
    
    def _extract_entities(self, message: str, language: str) -> List[Dict]:
        """
        Extract entities from the message.
        
        Args:
            message: Lowercase message text
            language: Language code
            
        Returns:
            List of entity dictionaries
        """
        entities = []
        
        # Check each entity pattern
        for entity_type, patterns in self.entity_patterns.items():
            if language in patterns:
                for pattern in patterns[language]:
                    matches = re.finditer(pattern, message, re.IGNORECASE)
                    for match in matches:
                        entities.append({
                            'type': entity_type,
                            'value': match.group(),
                            'start': match.start(),
                            'end': match.end(),
                            'confidence': 0.8
                        })
        
        # Remove duplicate entities
        unique_entities = []
        seen_values = set()
        for entity in entities:
            if entity['value'] not in seen_values:
                unique_entities.append(entity)
                seen_values.add(entity['value'])
        
        return unique_entities
    
    def get_supported_intents(self) -> List[str]:
        """Get list of supported intents."""
        return list(self.intent_patterns.keys())
    
    def get_intent_description(self, intent: str) -> str:
        """Get description of an intent."""
        descriptions = {
            'greeting': 'User is greeting or starting a conversation',
            'goodbye': 'User is ending the conversation',
            'attraction_info': 'User wants information about tourist attractions',
            'food_info': 'User wants information about local food and cuisine',
            'culture_info': 'User wants information about local culture and customs',
            'transport_info': 'User wants information about transportation options',
            'accommodation_info': 'User wants information about places to stay'
        }
        return descriptions.get(intent, 'Unknown intent')
    
    def get_entity_types(self) -> List[str]:
        """Get list of supported entity types."""
        return list(self.entity_patterns.keys())
    
    def validate_intent(self, intent: str) -> bool:
        """Check if an intent is supported."""
        return intent in self.intent_patterns
    
    def get_intent_examples(self, intent: str, language: str = 'en') -> List[str]:
        """Get example phrases for an intent in a specific language."""
        if intent not in self.intent_patterns or language not in self.intent_patterns[intent]:
            return []
        
        # Convert regex patterns to example phrases (simplified)
        examples = []
        patterns = self.intent_patterns[intent][language]
        
        for pattern in patterns:
            # Simple conversion of common patterns to examples
            example = pattern.replace(r'\b', '').replace(r'|', ' or ')
            if example and len(example) > 3:  # Filter out very short patterns
                examples.append(example)
        
        return examples[:5]  # Return max 5 examples