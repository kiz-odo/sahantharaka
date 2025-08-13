"""
Intent Recognition Module for Sri Lanka Tourism Chatbot

Recognizes user intents and extracts entities from tourist queries
"""

import re
from typing import Dict, List, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)

class IntentRecognizer:
    """
    Intent recognition system for tourism chatbot
    Supports multiple languages and tourism-specific intents
    """
    
    def __init__(self):
        self.intents = self._initialize_intents()
        self.entities = self._initialize_entities()
    
    def _initialize_intents(self) -> Dict[str, Any]:
        """Initialize intent patterns for all supported languages"""
        return {
            'greeting': {
                'en': [
                    r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b',
                    r'\b(how are you|how do you do)\b'
                ],
                'si': [
                    r'\b(ආයුබෝවන්|කොහොමද|සුභ දවසක්|සුභ උදෑසනක්|සුභ සවසක්)\b',
                    r'\b(කොහොමද ඉන්නේ)\b'
                ],
                'ta': [
                    r'\b(வணக்கம்|எப்படி இருக்கிறீர்கள்|காலை வணக்கம்|மாலை வணக்கம்)\b'
                ],
                'zh': [
                    r'\b(你好|您好|早上好|下午好|晚上好)\b'
                ],
                'fr': [
                    r'\b(bonjour|salut|bonsoir|comment allez-vous)\b'
                ]
            },
            'attraction_inquiry': {
                'en': [
                    r'\b(where|what|tell me about|show me|find|visit|see|attraction|place|destination|tourist spot)\b',
                    r'\b(temple|beach|mountain|fort|palace|museum|park|garden)\b',
                    r'\b(sigiriya|kandy|galle|ella|nuwara eliya|anuradhapura|polonnaruwa)\b'
                ],
                'si': [
                    r'\b(කොහෙද|මොකද|කියන්න|පෙන්වන්න|හොයන්න|බලන්න|ගමන් කරන්න|ස්ථානය|ප්‍රදේශය)\b',
                    r'\b(දේවාලය|වෙරළ|කන්ද|කොටුව|මාලිගය|කෞතුකාගාරය|උයන)\b',
                    r'\b(සීගිරිය|මහනුවර|ගාල්ල|ඇල්ල|නුවරඑළිය|අනුරාධපුරය|පොළොන්නරුව)\b'
                ],
                'ta': [
                    r'\b(எங்கே|என்ன|சொல்லுங்கள்|காட்டுங்கள்|தேடு|பார்வையிடு|இடம்|சுற்றுலா)\b',
                    r'\b(கோயில்|கடற்கரை|மலை|கோட்டை|அரண்மனை|அருங்காட்சியகம்|பூங்கா)\b'
                ],
                'zh': [
                    r'\b(哪里|什么|告诉我|显示|寻找|参观|景点|地方|旅游景点)\b',
                    r'\b(寺庙|海滩|山|堡垒|宫殿|博物馆|公园)\b'
                ],
                'fr': [
                    r'\b(où|quoi|dites-moi|montrez-moi|trouver|visiter|lieu|attraction|destination)\b',
                    r'\b(temple|plage|montagne|fort|palais|musée|parc|jardin)\b'
                ]
            },
            'food_inquiry': {
                'en': [
                    r'\b(food|eat|meal|dish|cuisine|restaurant|hungry|taste|spicy|curry|rice)\b',
                    r'\b(hopper|kottu|string hopper|roti|sambol|traditional food)\b'
                ],
                'si': [
                    r'\b(ආහාර|කන්න|කෑම|ව්‍යංජන|ආපනශාලා|බඩගිනි|රස|කාර කරි|බත්)\b',
                    r'\b(ආප්ප|කොත්තු|ඉදිආප්ප|රොටි|සම්බෝල|සාම්ප්‍රදායික ආහාර)\b'
                ],
                'ta': [
                    r'\b(உணவு|சாப்பிட|உணவு|உணவகம்|பசி|சுவை|காரம்|சாதம்|கறி)\b'
                ],
                'zh': [
                    r'\b(食物|吃|餐|菜|餐厅|饿|味道|辣|咖喱|米饭)\b'
                ],
                'fr': [
                    r'\b(nourriture|manger|repas|plat|cuisine|restaurant|faim|goût|épicé|curry|riz)\b'
                ]
            },
            'transport_inquiry': {
                'en': [
                    r'\b(transport|travel|how to get|go to|bus|train|taxi|tuk tuk|flight|airport)\b',
                    r'\b(ticket|booking|schedule|timetable|fare|price)\b'
                ],
                'si': [
                    r'\b(ප්‍රවාහනය|ගමන්|යන්නේ කොහොමද|යන්න|බස්|දුම්රිය|ටැක්සි|ත්‍රීරෝදය|ගුවන්|ගුවන්තොටුපළ)\b',
                    r'\b(ටිකට්|වන්දනාව|කාලසටහන|ගාස්තු|මිල)\b'
                ],
                'ta': [
                    r'\b(போக்குவரத்து|பயணம்|எப்படி செல்வது|செல்ல|பேரூந்து|ரயில்|டாக்ஸி|ஆட்டோ|விமானம்|விமான நிலையம்)\b'
                ],
                'zh': [
                    r'\b(交通|旅行|怎么去|去|公交|火车|出租车|嘟嘟车|飞机|机场)\b'
                ],
                'fr': [
                    r'\b(transport|voyage|comment aller|aller|bus|train|taxi|tuk tuk|vol|aéroport)\b'
                ]
            },
            'accommodation_inquiry': {
                'en': [
                    r'\b(hotel|accommodation|stay|room|booking|guesthouse|resort|lodge)\b',
                    r'\b(where to stay|place to sleep|budget hotel|luxury hotel)\b'
                ],
                'si': [
                    r'\b(හෝටලය|නවාතැන්|ඉන්න|කාමරය|වන්දනාව|ගෘහ නවාතැන්|නිකේතනය)\b',
                    r'\b(ඉන්න තැන|නිදන තැන|අඩු මිල හෝටල්|සුඛෝපභෝගී හෝටල්)\b'
                ],
                'ta': [
                    r'\b(ஹோட்டல்|தங்குமிடம்|தங்க|அறை|முன்பதிவு|விருந்தினர் இல்லம்|ரிசார்ட்)\b'
                ],
                'zh': [
                    r'\b(酒店|住宿|住|房间|预订|客栈|度假村)\b'
                ],
                'fr': [
                    r'\b(hôtel|hébergement|rester|chambre|réservation|pension|resort)\b'
                ]
            },
            'weather_inquiry': {
                'en': [
                    r'\b(weather|climate|temperature|rain|sunny|hot|cold|season|monsoon)\b',
                    r'\b(what\'s the weather|how\'s the weather|weather forecast)\b'
                ],
                'si': [
                    r'\b(කාලගුණය|දේශගුණය|උෂ්ණත්වය|වර්ෂාව|අව්ව|උණුසුම්|සීතල|කාලය|මෝසම්)\b',
                    r'\b(කාලගුණය කොහොමද|කාලගුණ අනාවැකිය)\b'
                ],
                'ta': [
                    r'\b(வானிலை|காலநிலை|வெப்பநிலை|மழை|வெயில்|சூடு|குளிர்|பருவம்|பருவமழை)\b'
                ],
                'zh': [
                    r'\b(天气|气候|温度|雨|晴天|热|冷|季节|季风)\b'
                ],
                'fr': [
                    r'\b(météo|climat|température|pluie|ensoleillé|chaud|froid|saison|mousson)\b'
                ]
            },
            'help_inquiry': {
                'en': [
                    r'\b(help|assist|support|guide|confused|lost|don\'t know|problem)\b',
                    r'\b(can you help|need help|what can you do)\b'
                ],
                'si': [
                    r'\b(උදව්|සහාය|මග පෙන්වන්න|අවුල්|අහුම්|දන්නේ නෑ|ප්‍රශ්නය)\b',
                    r'\b(උදව් කරන්න පුළුවන්ද|උදව් ඕනේ|මොනාද කරන්න පුළුවන්)\b'
                ],
                'ta': [
                    r'\b(உதவி|பணி|ஆதரவு|வழிகாட்டி|குழப்பம்|தொலைந்தேன்|தெரியாது|பிரச்சனை)\b'
                ],
                'zh': [
                    r'\b(帮助|协助|支持|指导|困惑|迷路|不知道|问题)\b'
                ],
                'fr': [
                    r'\b(aide|assister|soutien|guide|confus|perdu|ne sais pas|problème)\b'
                ]
            },
            'goodbye': {
                'en': [
                    r'\b(goodbye|bye|see you|farewell|thanks|thank you|exit|quit)\b'
                ],
                'si': [
                    r'\b(ගිහින් එන්නම්|බයි|ආයේ හමුවෙමු|ස්තූතියි|ස්තූති|යන්නම්)\b'
                ],
                'ta': [
                    r'\b(விடைபெறுகிறேன்|பை|மீண்டும் சந்திப்போம்|நன்றி|வெளியேறு)\b'
                ],
                'zh': [
                    r'\b(再见|拜拜|再会|谢谢|退出)\b'
                ],
                'fr': [
                    r'\b(au revoir|bye|à bientôt|merci|sortir|quitter)\b'
                ]
            }
        }
    
    def _initialize_entities(self) -> Dict[str, Any]:
        """Initialize entity extraction patterns"""
        return {
            'locations': {
                'cities': [
                    'colombo', 'kandy', 'galle', 'jaffna', 'batticaloa', 'matara', 'negombo',
                    'nuwara eliya', 'ella', 'sigiriya', 'dambulla', 'anuradhapura', 'polonnaruwa',
                    'trincomalee', 'bentota', 'hikkaduwa', 'mirissa', 'unawatuna', 'arugam bay'
                ],
                'attractions': [
                    'sigiriya', 'temple of tooth', 'galle fort', 'yala national park',
                    'horton plains', 'adams peak', 'nine arch bridge', 'royal botanical gardens',
                    'pinnawala elephant orphanage', 'dambulla cave temple'
                ]
            },
            'time_expressions': [
                r'\b(today|tomorrow|yesterday|next week|this week|weekend)\b',
                r'\b(morning|afternoon|evening|night)\b',
                r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
                r'\b(\d{1,2}[th|st|nd|rd]?\s+(january|february|march|april|may|june|july|august|september|october|november|december))\b'
            ],
            'budget_expressions': [
                r'\b(budget|cheap|expensive|luxury|mid-range|affordable)\b',
                r'\b(under \$?\d+|less than \$?\d+|around \$?\d+|about \$?\d+)\b',
                r'\b(\$\d+|\d+ dollars|\d+ rupees|LKR \d+)\b'
            ],
            'duration_expressions': [
                r'\b(\d+\s+(day|days|week|weeks|month|months))\b',
                r'\b(few days|several days|one week|two weeks)\b'
            ]
        }
    
    def recognize_intent(self, text: str, language: str = 'en') -> Tuple[str, float]:
        """
        Recognize the intent of user input
        
        Args:
            text (str): User input text
            language (str): Language code
            
        Returns:
            Tuple[str, float]: Intent name and confidence score
        """
        if not text or not text.strip():
            return 'unknown', 0.0
        
        text_lower = text.lower()
        intent_scores = {}
        
        # Check each intent pattern
        for intent_name, language_patterns in self.intents.items():
            patterns = language_patterns.get(language, language_patterns.get('en', []))
            score = 0.0
            
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                if matches > 0:
                    score += min(matches * 0.3, 1.0)
            
            if score > 0:
                intent_scores[intent_name] = min(score, 1.0)
        
        if not intent_scores:
            return 'unknown', 0.0
        
        # Find the intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        confidence = intent_scores[best_intent]
        
        logger.info(f"Recognized intent: {best_intent} with confidence: {confidence:.2f}")
        
        return best_intent, confidence
    
    def extract_entities(self, text: str, intent: str = None) -> Dict[str, List[str]]:
        """
        Extract entities from user input
        
        Args:
            text (str): User input text
            intent (str): Recognized intent (optional)
            
        Returns:
            Dict[str, List[str]]: Extracted entities by type
        """
        entities = {}
        text_lower = text.lower()
        
        # Extract locations
        locations = []
        for city in self.entities['locations']['cities']:
            if city in text_lower:
                locations.append(city)
        
        for attraction in self.entities['locations']['attractions']:
            if attraction in text_lower:
                locations.append(attraction)
        
        if locations:
            entities['locations'] = list(set(locations))
        
        # Extract time expressions
        time_expressions = []
        for pattern in self.entities['time_expressions']:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            time_expressions.extend(matches)
        
        if time_expressions:
            entities['time'] = list(set(time_expressions))
        
        # Extract budget expressions
        budget_expressions = []
        for pattern in self.entities['budget_expressions']:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            budget_expressions.extend(matches)
        
        if budget_expressions:
            entities['budget'] = list(set(budget_expressions))
        
        # Extract duration expressions
        duration_expressions = []
        for pattern in self.entities['duration_expressions']:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            duration_expressions.extend(matches)
        
        if duration_expressions:
            entities['duration'] = list(set(duration_expressions))
        
        logger.info(f"Extracted entities: {entities}")
        
        return entities
    
    def get_intent_examples(self, intent: str, language: str = 'en') -> List[str]:
        """
        Get example phrases for a specific intent
        
        Args:
            intent (str): Intent name
            language (str): Language code
            
        Returns:
            List[str]: Example phrases
        """
        examples = {
            'greeting': {
                'en': ['Hello!', 'Hi there!', 'Good morning!', 'How are you?'],
                'si': ['ආයුබෝවන්!', 'කොහොමද?', 'සුභ උදෑසනක්!'],
                'ta': ['வணக்கம்!', 'எப்படி இருக்கிறீர்கள்?'],
                'zh': ['你好!', '早上好!'],
                'fr': ['Bonjour!', 'Comment allez-vous?']
            },
            'attraction_inquiry': {
                'en': ['What can I visit in Kandy?', 'Tell me about Sigiriya', 'Where are the best temples?'],
                'si': ['මහනුවරේ මොනාද බලන්න තියෙන්නේ?', 'සීගිරිය ගැන කියන්න'],
                'ta': ['கண்டியில் என்ன பார்க்கலாம்?', 'சிகிரியா பற்றி சொல்லுங்கள்'],
                'zh': ['康提有什么可以参观的?', '告诉我关于狮子岩的信息'],
                'fr': ['Que puis-je visiter à Kandy?', 'Parlez-moi de Sigiriya']
            }
        }
        
        return examples.get(intent, {}).get(language, examples.get(intent, {}).get('en', []))
    
    def get_supported_intents(self) -> List[str]:
        """
        Get list of supported intents
        
        Returns:
            List[str]: List of intent names
        """
        return list(self.intents.keys())