"""
Advanced NLP & Machine Learning Component

Provides advanced natural language processing capabilities including
context understanding, intent prediction, sentiment analysis, and
language generation for Phase 3 of the chatbot.
"""

import logging
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import defaultdict, Counter

try:
    import spacy
    SPACY_AVAILABLE = True
    # Load English model
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = None
        logging.warning("spaCy English model not available")
except ImportError:
    SPACY_AVAILABLE = False
    nlp = None
    logging.warning("spaCy not available, advanced NLP features disabled")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logging.warning("TextBlob not available, sentiment analysis disabled")

logger = logging.getLogger(__name__)


class IntentType(Enum):
    """Types of user intents."""
    GREETING = "greeting"
    FAREWELL = "farewell"
    QUESTION = "question"
    REQUEST = "request"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    CLARIFICATION = "clarification"
    CONFIRMATION = "confirmation"
    NEGATION = "negation"
    AFFIRMATION = "affirmation"


class SentimentType(Enum):
    """Types of sentiment."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class ContextType(Enum):
    """Types of conversation context."""
    LOCATION = "location"
    TIME = "time"
    USER_PREFERENCE = "user_preference"
    CONVERSATION_HISTORY = "conversation_history"
    EMOTIONAL_STATE = "emotional_state"
    INTENT_HISTORY = "intent_history"


@dataclass
class IntentResult:
    """Result of intent detection."""
    intent: str
    confidence: float
    entities: List[Dict[str, Any]]
    context: Dict[str, Any]
    alternatives: List[Tuple[str, float]]


@dataclass
class SentimentResult:
    """Result of sentiment analysis."""
    sentiment: SentimentType
    confidence: float
    polarity: float
    subjectivity: float
    emotions: Dict[str, float]


@dataclass
class ContextualResponse:
    """Contextual response with metadata."""
    text: str
    language: str
    context_used: List[str]
    confidence: float
    alternatives: List[str]
    metadata: Dict[str, Any]


class AdvancedNLPEngine:
    """
    Advanced NLP engine providing context understanding, intent prediction,
    sentiment analysis, and intelligent response generation.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the advanced NLP engine.
        
        Args:
            config: Configuration dictionary for NLP settings
        """
        self.config = config or {}
        self.conversation_contexts = defaultdict(dict)
        self.intent_patterns = self._initialize_intent_patterns()
        self.entity_patterns = self._initialize_entity_patterns()
        self.context_rules = self._initialize_context_rules()
        
        # NLP models and settings
        self.min_confidence = self.config.get('min_confidence', 0.7)
        self.context_window = self.config.get('context_window', 5)
        self.sentiment_threshold = self.config.get('sentiment_threshold', 0.1)
        
        # Language models
        self.language_models = {
            'en': self._load_english_model(),
            'si': self._load_sinhala_model(),
            'ta': self._load_tamil_model()
        }
        
        logger.info("Advanced NLP Engine initialized successfully")
    
    def _load_english_model(self):
        """Load English language model."""
        if SPACY_AVAILABLE and nlp:
            return nlp
        return None
    
    def _load_sinhala_model(self):
        """Load Sinhala language model (placeholder)."""
        # In production, load proper Sinhala model
        return None
    
    def _load_tamil_model(self):
        """Load Tamil language model (placeholder)."""
        # In production, load proper Tamil model
        return None
    
    def _initialize_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize intent recognition patterns."""
        patterns = {
            IntentType.GREETING.value: [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\b(ayubowan|vanakkam|namaste)\b',
                r'\b(how are you|how\'s it going)\b'
            ],
            IntentType.FAREWELL.value: [
                r'\b(bye|goodbye|see you|take care|farewell)\b',
                r'\b(mata saman|nandri|dhanyawad)\b'
            ],
            IntentType.QUESTION.value: [
                r'\b(what|where|when|who|why|how)\b',
                r'\b(can you|could you|would you)\b',
                r'\b(tell me|explain|describe)\b'
            ],
            IntentType.REQUEST.value: [
                r'\b(please|help|need|want|looking for)\b',
                r'\b(show me|find|search|recommend)\b'
            ],
            IntentType.COMPLAINT.value: [
                r'\b(problem|issue|wrong|not working|broken)\b',
                r'\b(bad|terrible|awful|disappointed)\b'
            ],
            IntentType.COMPLIMENT.value: [
                r'\b(great|amazing|wonderful|excellent|fantastic)\b',
                r'\b(thank you|thanks|appreciate|love it)\b'
            ]
        }
        return patterns
    
    def _initialize_entity_patterns(self) -> Dict[str, List[str]]:
        """Initialize entity extraction patterns."""
        patterns = {
            'location': [
                r'\b(sigiriya|kandy|colombo|galle|anuradhapura|polonnaruwa)\b',
                r'\b(central province|southern province|western province)\b'
            ],
            'time': [
                r'\b(today|tomorrow|yesterday|morning|afternoon|evening)\b',
                r'\b(week|month|year|season|festival)\b'
            ],
            'activity': [
                r'\b(hiking|swimming|sightseeing|shopping|eating|drinking)\b',
                r'\b(visit|explore|see|experience|enjoy)\b'
            ],
            'food': [
                r'\b(rice|curry|hoppers|string hoppers|kottu|roti)\b',
                r'\b(tea|coffee|juice|water|beer|wine)\b'
            ]
        }
        return patterns
    
    def _initialize_context_rules(self) -> Dict[str, Any]:
        """Initialize context understanding rules."""
        rules = {
            'location_context': {
                'keywords': ['here', 'this place', 'nearby', 'around'],
                'fallback': 'current_location',
                'confidence_boost': 0.2
            },
            'time_context': {
                'keywords': ['now', 'currently', 'at the moment'],
                'fallback': 'current_time',
                'confidence_boost': 0.15
            },
            'user_preference_context': {
                'keywords': ['like', 'prefer', 'favorite', 'enjoy'],
                'fallback': 'user_preferences',
                'confidence_boost': 0.25
            }
        }
        return rules
    
    def process_message(self, message: str, user_id: str, 
                       language: str = 'en',
                       conversation_history: List[Dict] = None) -> IntentResult:
        """
        Process a user message with advanced NLP capabilities.
        
        Args:
            message: User message text
            user_id: User identifier
            language: Message language
            conversation_history: Previous conversation context
            
        Returns:
            IntentResult with detected intent and context
        """
        try:
            # Preprocess message
            processed_message = self._preprocess_message(message, language)
            
            # Detect intent
            intent, confidence = self._detect_intent(processed_message, language)
            
            # Extract entities
            entities = self._extract_entities(processed_message, language)
            
            # Analyze sentiment
            sentiment = self._analyze_sentiment(processed_message, language)
            
            # Build context
            context = self._build_context(user_id, message, intent, entities, 
                                        sentiment, conversation_history)
            
            # Get alternative intents
            alternatives = self._get_alternative_intents(processed_message, language)
            
            # Update conversation context
            self._update_conversation_context(user_id, intent, context, confidence)
            
            return IntentResult(
                intent=intent,
                confidence=confidence,
                entities=entities,
                context=context,
                alternatives=alternatives
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return IntentResult(
                intent='unknown',
                confidence=0.0,
                entities=[],
                context={},
                alternatives=[]
            )
    
    def _preprocess_message(self, message: str, language: str) -> str:
        """Preprocess message for NLP analysis."""
        try:
            # Convert to lowercase for English
            if language == 'en':
                message = message.lower()
            
            # Remove extra whitespace
            message = re.sub(r'\s+', ' ', message).strip()
            
            # Remove special characters (keep basic punctuation)
            if language == 'en':
                message = re.sub(r'[^\w\s\.\?\!\,\-]', '', message)
            
            return message
            
        except Exception as e:
            logger.error(f"Error preprocessing message: {str(e)}")
            return message
    
    def _detect_intent(self, message: str, language: str) -> Tuple[str, float]:
        """Detect user intent using multiple methods."""
        try:
            # Method 1: Pattern matching
            pattern_score, pattern_intent = self._detect_intent_by_patterns(message, language)
            
            # Method 2: Keyword analysis
            keyword_score, keyword_intent = self._detect_intent_by_keywords(message, language)
            
            # Method 3: Contextual analysis
            context_score, context_intent = self._detect_intent_by_context(message, language)
            
            # Combine scores
            scores = [
                (pattern_score, pattern_intent),
                (keyword_score, keyword_intent),
                (context_score, context_intent)
            ]
            
            # Remove None intents
            scores = [(score, intent) for score, intent in scores if intent is not None]
            
            if not scores:
                return 'unknown', 0.0
            
            # Weighted combination
            total_score = 0.0
            weighted_intents = defaultdict(float)
            
            for score, intent in scores:
                weighted_intents[intent] += score
                total_score += score
            
            # Get best intent
            best_intent = max(weighted_intents.items(), key=lambda x: x[1])
            
            # Normalize confidence
            confidence = best_intent[1] / total_score if total_score > 0 else 0.0
            
            return best_intent[0], confidence
            
        except Exception as e:
            logger.error(f"Error detecting intent: {str(e)}")
            return 'unknown', 0.0
    
    def _detect_intent_by_patterns(self, message: str, language: str) -> Tuple[float, Optional[str]]:
        """Detect intent using regex patterns."""
        try:
            best_score = 0.0
            best_intent = None
            
            for intent, patterns in self.intent_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, message, re.IGNORECASE)
                    if matches:
                        score = len(matches) / len(patterns)
                        if score > best_score:
                            best_score = score
                            best_intent = intent
            
            return best_score, best_intent
            
        except Exception as e:
            logger.error(f"Error detecting intent by patterns: {str(e)}")
            return 0.0, None
    
    def _detect_intent_by_keywords(self, message: str, language: str) -> Tuple[float, Optional[str]]:
        """Detect intent using keyword analysis."""
        try:
            # Define keyword weights for each intent
            keyword_weights = {
                IntentType.GREETING.value: ['hello', 'hi', 'hey', 'good'],
                IntentType.QUESTION.value: ['what', 'where', 'when', 'how', 'why'],
                IntentType.REQUEST.value: ['help', 'need', 'want', 'please'],
                IntentType.COMPLAINT.value: ['problem', 'issue', 'wrong', 'bad'],
                IntentType.COMPLIMENT.value: ['great', 'amazing', 'thank', 'love']
            }
            
            best_score = 0.0
            best_intent = None
            
            for intent, keywords in keyword_weights.items():
                score = 0.0
                for keyword in keywords:
                    if keyword.lower() in message.lower():
                        score += 1.0
                
                if score > 0:
                    score = score / len(keywords)
                    if score > best_score:
                        best_score = score
                        best_intent = intent
            
            return best_score, best_intent
            
        except Exception as e:
            logger.error(f"Error detecting intent by keywords: {str(e)}")
            return 0.0, None
    
    def _detect_intent_by_context(self, message: str, language: str) -> Tuple[float, Optional[str]]:
        """Detect intent using contextual analysis."""
        try:
            # This is a simplified context analysis
            # In production, use more sophisticated context understanding
            
            # Check for follow-up questions
            if any(word in message.lower() for word in ['also', 'too', 'as well', 'additionally']):
                return 0.8, IntentType.QUESTION.value
            
            # Check for clarifications
            if any(word in message.lower() for word in ['what do you mean', 'can you explain', 'i don\'t understand']):
                return 0.9, IntentType.CLARIFICATION.value
            
            # Check for confirmations
            if any(word in message.lower() for word in ['is that right', 'are you sure', 'really']):
                return 0.8, IntentType.CONFIRMATION.value
            
            return 0.0, None
            
        except Exception as e:
            logger.error(f"Error detecting intent by context: {str(e)}")
            return 0.0, None
    
    def _extract_entities(self, message: str, language: str) -> List[Dict[str, Any]]:
        """Extract entities from message."""
        try:
            entities = []
            
            # Extract entities using patterns
            for entity_type, patterns in self.entity_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, message, re.IGNORECASE)
                    for match in matches:
                        entities.append({
                            'type': entity_type,
                            'value': match.group(),
                            'start': match.start(),
                            'end': match.end(),
                            'confidence': 0.8
                        })
            
            # Extract entities using spaCy (if available)
            if SPACY_AVAILABLE and nlp and language == 'en':
                spacy_entities = self._extract_entities_with_spacy(message)
                entities.extend(spacy_entities)
            
            # Remove duplicates and sort by position
            unique_entities = []
            seen_values = set()
            
            for entity in sorted(entities, key=lambda x: x['start']):
                if entity['value'] not in seen_values:
                    unique_entities.append(entity)
                    seen_values.add(entity['value'])
            
            return unique_entities
            
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return []
    
    def _extract_entities_with_spacy(self, message: str) -> List[Dict[str, Any]]:
        """Extract entities using spaCy."""
        try:
            if not nlp:
                return []
            
            doc = nlp(message)
            entities = []
            
            for ent in doc.ents:
                entities.append({
                    'type': ent.label_.lower(),
                    'value': ent.text,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'confidence': 0.9
                })
            
            return entities
            
        except Exception as e:
            logger.error(f"Error extracting entities with spaCy: {str(e)}")
            return []
    
    def _analyze_sentiment(self, message: str, language: str) -> SentimentResult:
        """Analyze message sentiment."""
        try:
            if TEXTBLOB_AVAILABLE and language == 'en':
                return self._analyze_sentiment_with_textblob(message)
            else:
                return self._analyze_sentiment_with_patterns(message, language)
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return SentimentResult(
                sentiment=SentimentType.NEUTRAL,
                confidence=0.5,
                polarity=0.0,
                subjectivity=0.5,
                emotions={}
            )
    
    def _analyze_sentiment_with_textblob(self, message: str) -> SentimentResult:
        """Analyze sentiment using TextBlob."""
        try:
            blob = TextBlob(message)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment type
            if polarity > self.sentiment_threshold:
                sentiment = SentimentType.POSITIVE
            elif polarity < -self.sentiment_threshold:
                sentiment = SentimentType.NEGATIVE
            else:
                sentiment = SentimentType.NEUTRAL
            
            # Calculate confidence based on subjectivity
            confidence = 1.0 - subjectivity
            
            # Extract emotions (simplified)
            emotions = self._extract_emotions(message)
            
            return SentimentResult(
                sentiment=sentiment,
                confidence=confidence,
                polarity=polarity,
                subjectivity=subjectivity,
                emotions=emotions
            )
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment with TextBlob: {str(e)}")
            return SentimentResult(
                sentiment=SentimentType.NEUTRAL,
                confidence=0.5,
                polarity=0.0,
                subjectivity=0.5,
                emotions={}
            )
    
    def _analyze_sentiment_with_patterns(self, message: str, language: str) -> SentimentResult:
        """Analyze sentiment using pattern matching."""
        try:
            # Define sentiment patterns
            positive_patterns = [
                r'\b(good|great|excellent|amazing|wonderful|fantastic|awesome)\b',
                r'\b(love|like|enjoy|happy|pleased|satisfied)\b',
                r'\b(thank|thanks|appreciate|grateful)\b'
            ]
            
            negative_patterns = [
                r'\b(bad|terrible|awful|horrible|disappointing|frustrated)\b',
                r'\b(hate|dislike|angry|upset|sad|worried)\b',
                r'\b(problem|issue|wrong|broken|failed)\b'
            ]
            
            # Count matches
            positive_count = sum(len(re.findall(pattern, message, re.IGNORECASE)) 
                               for pattern in positive_patterns)
            negative_count = sum(len(re.findall(pattern, message, re.IGNORECASE)) 
                               for pattern in negative_patterns)
            
            # Determine sentiment
            if positive_count > negative_count:
                sentiment = SentimentType.POSITIVE
                polarity = min(positive_count / 10, 1.0)
            elif negative_count > positive_count:
                sentiment = SentimentType.NEGATIVE
                polarity = -min(negative_count / 10, 1.0)
            else:
                sentiment = SentimentType.NEUTRAL
                polarity = 0.0
            
            # Calculate confidence
            total_matches = positive_count + negative_count
            confidence = min(total_matches / 5, 1.0) if total_matches > 0 else 0.5
            
            # Extract emotions
            emotions = self._extract_emotions(message)
            
            return SentimentResult(
                sentiment=sentiment,
                confidence=confidence,
                polarity=polarity,
                subjectivity=0.5,
                emotions=emotions
            )
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment with patterns: {str(e)}")
            return SentimentResult(
                sentiment=SentimentType.NEUTRAL,
                confidence=0.5,
                polarity=0.0,
                subjectivity=0.5,
                emotions={}
            )
    
    def _extract_emotions(self, message: str) -> Dict[str, float]:
        """Extract emotions from message."""
        try:
            emotions = {
                'joy': 0.0,
                'sadness': 0.0,
                'anger': 0.0,
                'fear': 0.0,
                'surprise': 0.0,
                'disgust': 0.0
            }
            
            # Emotion keywords
            emotion_keywords = {
                'joy': ['happy', 'joy', 'excited', 'thrilled', 'delighted'],
                'sadness': ['sad', 'depressed', 'melancholy', 'gloomy', 'sorrow'],
                'anger': ['angry', 'furious', 'irritated', 'annoyed', 'mad'],
                'fear': ['afraid', 'scared', 'terrified', 'worried', 'anxious'],
                'surprise': ['surprised', 'amazed', 'astonished', 'shocked', 'stunned'],
                'disgust': ['disgusted', 'revolted', 'appalled', 'repulsed', 'sickened']
            }
            
            # Count emotion keywords
            for emotion, keywords in emotion_keywords.items():
                count = sum(len(re.findall(rf'\b{keyword}\b', message, re.IGNORECASE)) 
                           for keyword in keywords)
                if count > 0:
                    emotions[emotion] = min(count / 3, 1.0)
            
            return emotions
            
        except Exception as e:
            logger.error(f"Error extracting emotions: {str(e)}")
            return {}
    
    def _build_context(self, user_id: str, message: str, intent: str,
                       entities: List[Dict], sentiment: SentimentResult,
                       conversation_history: List[Dict]) -> Dict[str, Any]:
        """Build conversation context."""
        try:
            context = {
                'user_id': user_id,
                'timestamp': datetime.now(),
                'intent': intent,
                'entities': entities,
                'sentiment': sentiment.sentiment.value,
                'sentiment_confidence': sentiment.confidence,
                'emotions': sentiment.emotions
            }
            
            # Add location context
            location_entities = [e for e in entities if e['type'] == 'location']
            if location_entities:
                context['location'] = location_entities[0]['value']
            
            # Add time context
            time_entities = [e for e in entities if e['type'] == 'time']
            if time_entities:
                context['time_reference'] = time_entities[0]['value']
            
            # Add conversation history context
            if conversation_history:
                recent_context = self._extract_recent_context(conversation_history)
                context.update(recent_context)
            
            # Add user preference context
            user_prefs = self._get_user_preferences(user_id)
            if user_prefs:
                context['user_preferences'] = user_prefs
            
            return context
            
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            return {'user_id': user_id, 'timestamp': datetime.now()}
    
    def _extract_recent_context(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """Extract context from recent conversation history."""
        try:
            recent_context = {}
            
            # Get last few messages
            recent_messages = conversation_history[-self.context_window:]
            
            # Extract common topics
            topics = []
            for msg in recent_messages:
                if 'entities' in msg:
                    topics.extend([e['value'] for e in msg['entities']])
            
            if topics:
                topic_counts = Counter(topics)
                recent_context['common_topics'] = topic_counts.most_common(3)
            
            # Extract intent patterns
            intents = [msg.get('intent', 'unknown') for msg in recent_messages]
            if intents:
                intent_counts = Counter(intents)
                recent_context['intent_pattern'] = intent_counts.most_common(1)[0][0]
            
            # Extract sentiment trend
            sentiments = [msg.get('sentiment', 'neutral') for msg in recent_messages]
            if sentiments:
                sentiment_counts = Counter(sentiments)
                recent_context['sentiment_trend'] = sentiment_counts.most_common(1)[0][0]
            
            return recent_context
            
        except Exception as e:
            logger.error(f"Error extracting recent context: {str(e)}")
            return {}
    
    def _get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences for context building."""
        try:
            # This is a placeholder - integrate with user profile system
            return {}
        except Exception as e:
            logger.error(f"Error getting user preferences: {str(e)}")
            return {}
    
    def _get_alternative_intents(self, message: str, language: str) -> List[Tuple[str, float]]:
        """Get alternative intent predictions."""
        try:
            alternatives = []
            
            # Get all intent scores
            intent_scores = {}
            
            # Pattern-based scores
            pattern_score, pattern_intent = self._detect_intent_by_patterns(message, language)
            if pattern_intent:
                intent_scores[pattern_intent] = pattern_score
            
            # Keyword-based scores
            keyword_score, keyword_intent = self._detect_intent_by_keywords(message, language)
            if keyword_intent:
                intent_scores[keyword_intent] = keyword_score
            
            # Context-based scores
            context_score, context_intent = self._detect_intent_by_context(message, language)
            if context_intent:
                intent_scores[context_intent] = context_score
            
            # Sort by score and return top alternatives
            sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
            
            for intent, score in sorted_intents[1:4]:  # Skip the best one
                if score > 0.3:  # Minimum threshold
                    alternatives.append((intent, score))
            
            return alternatives
            
        except Exception as e:
            logger.error(f"Error getting alternative intents: {str(e)}")
            return []
    
    def _update_conversation_context(self, user_id: str, intent: str, 
                                   context: Dict[str, Any], confidence: float):
        """Update conversation context for user."""
        try:
            if user_id not in self.conversation_contexts:
                self.conversation_contexts[user_id] = {}
            
            user_context = self.conversation_contexts[user_id]
            
            # Update intent history
            if 'intent_history' not in user_context:
                user_context['intent_history'] = []
            
            user_context['intent_history'].append({
                'intent': intent,
                'confidence': confidence,
                'timestamp': datetime.now()
            })
            
            # Keep only recent history
            if len(user_context['intent_history']) > 10:
                user_context['intent_history'] = user_context['intent_history'][-10:]
            
            # Update current context
            user_context['current_context'] = context
            user_context['last_updated'] = datetime.now()
            
        except Exception as e:
            logger.error(f"Error updating conversation context: {str(e)}")
    
    def generate_contextual_response(self, intent: str, context: Dict[str, Any],
                                   language: str = 'en') -> ContextualResponse:
        """Generate contextual response based on intent and context."""
        try:
            # This is a simplified response generation
            # In production, use more sophisticated NLG models
            
            response_text = self._generate_basic_response(intent, context, language)
            
            # Enhance with context
            enhanced_response = self._enhance_response_with_context(response_text, context, language)
            
            return ContextualResponse(
                text=enhanced_response,
                language=language,
                context_used=list(context.keys()),
                confidence=0.8,
                alternatives=[],
                metadata={'generation_method': 'rule_based'}
            )
            
        except Exception as e:
            logger.error(f"Error generating contextual response: {str(e)}")
            return ContextualResponse(
                text="I'm sorry, I didn't understand that.",
                language=language,
                context_used=[],
                confidence=0.0,
                alternatives=[],
                metadata={'error': str(e)}
            )
    
    def _generate_basic_response(self, intent: str, context: Dict[str, Any], language: str) -> str:
        """Generate basic response for intent."""
        try:
            responses = {
                IntentType.GREETING.value: {
                    'en': "Hello! How can I help you today?",
                    'si': "ආයුබෝවන්! මට ඔබට උදව් කළ හැක්කේ කෙසේද?",
                    'ta': "வணக்கம்! இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?"
                },
                IntentType.QUESTION.value: {
                    'en': "I'd be happy to answer your question. What would you like to know?",
                    'si': "ඔබගේ ප්‍රශ්නයට පිළිතුරු දීමට මට සතුටුයි. ඔබ දැනගැනීමට අවශ්‍ය කරන්නේ කුමක්ද?",
                    'ta': "உங்கள் கேள்விக்கு பதிலளிக்க நான் மகிழ்ச்சியடைவேன். நீங்கள் என்ன தெரிந்து கொள்ள விரும்புகிறீர்கள்?"
                },
                IntentType.REQUEST.value: {
                    'en': "I'll do my best to help you. What do you need?",
                    'si': "ඔබට උදව් කිරීමට මම මගේ හොඳම උත්සාහය ගනිමි. ඔබට අවශ්‍ය කරන්නේ කුමක්ද?",
                    'ta': "உங்களுக்கு உதவ நான் எனது சிறந்த முயற்சியை செய்வேன். உங்களுக்கு என்ன தேவை?"
                }
            }
            
            if intent in responses and language in responses[intent]:
                return responses[intent][language]
            
            # Default response
            default_responses = {
                'en': "I understand. How can I assist you further?",
                'si': "මම තේරුම් ගනිමි. මට ඔබට තවදුරටත් උදව් කළ හැක්කේ කෙසේද?",
                'ta': "நான் புரிந்துகொள்கிறேன். நான் உங்களுக்கு மேலும் எப்படி உதவ முடியும்?"
            }
            
            return default_responses.get(language, default_responses['en'])
            
        except Exception as e:
            logger.error(f"Error generating basic response: {str(e)}")
            return "I'm sorry, I didn't understand that."
    
    def _enhance_response_with_context(self, response: str, context: Dict[str, Any], 
                                     language: str) -> str:
        """Enhance response with contextual information."""
        try:
            enhanced_response = response
            
            # Add location context
            if 'location' in context:
                location = context['location']
                if language == 'en':
                    enhanced_response += f" I see you're interested in {location}."
                elif language == 'si':
                    enhanced_response += f" ඔබ {location} ගැන උනන්දු වන බව මම දකිමි."
                elif language == 'ta':
                    enhanced_response += f" நீங்கள் {location} பற்றி ஆர்வமாக இருப்பதை நான் பார்க்கிறேன்."
            
            # Add time context
            if 'time_reference' in context:
                time_ref = context['time_reference']
                if language == 'en':
                    enhanced_response += f" Regarding {time_ref}, let me help you with that."
                elif language == 'si':
                    enhanced_response += f" {time_ref} සම්බන්ධයෙන්, මට ඔබට උදව් කිරීමට ඉඩ දෙන්න."
                elif language == 'ta':
                    enhanced_response += f" {time_ref} குறித்து, அதில் உங்களுக்கு உதவ அனுமதிக்கவும்."
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error enhancing response with context: {str(e)}")
            return response
    
    def get_nlp_stats(self) -> Dict[str, Any]:
        """Get NLP engine statistics."""
        return {
            'total_users': len(self.conversation_contexts),
            'supported_languages': list(self.language_models.keys()),
            'intent_patterns': len(self.intent_patterns),
            'entity_patterns': len(self.entity_patterns),
            'context_rules': len(self.context_rules),
            'spacy_available': SPACY_AVAILABLE,
            'textblob_available': TEXTBLOB_AVAILABLE
        }