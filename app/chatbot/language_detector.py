"""
Language Detection Module for Sri Lanka Tourism Chatbot

Supports detection of 5 languages: English, Sinhala, Tamil, Chinese, and French
"""

import re
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class LanguageDetector:
    """
    Advanced language detection for tourism chatbot
    Supports English, Sinhala, Tamil, Chinese, and French
    """
    
    def __init__(self):
        self.supported_languages = ['en', 'si', 'ta', 'zh', 'fr']
        self.language_names = {
            'en': 'English',
            'si': 'Sinhala',
            'ta': 'Tamil',
            'zh': 'Chinese',
            'fr': 'French'
        }
        
        # Language-specific patterns and keywords
        self.language_patterns = {
            'si': {
                'unicode_range': r'[\u0D80-\u0DFF]',
                'keywords': ['ආයුබෝවන්', 'ගමන්', 'කොහෙද', 'මොකද', 'කුමන', 'ගැන', 'එක්ක', 'කරන්න'],
                'greeting_patterns': [r'ආයුබෝවන්', r'කොහොමද', r'සුභ දවසක්']
            },
            'ta': {
                'unicode_range': r'[\u0B80-\u0BFF]',
                'keywords': ['வணக்கம்', 'எப்படி', 'எங்கே', 'என்ன', 'சுற்றுலா', 'இடம்', 'செல்ல', 'உதவி'],
                'greeting_patterns': [r'வணக்கம்', r'எப்படி', r'நன்றி']
            },
            'zh': {
                'unicode_range': r'[\u4e00-\u9fff]',
                'keywords': ['你好', '旅游', '哪里', '什么', '怎么', '帮助', '地方', '景点'],
                'greeting_patterns': [r'你好', r'您好', r'谢谢']
            },
            'fr': {
                'unicode_range': r'[a-zA-ZàâäéèêëïîôöùûüÿÀÂÄÉÈÊËÏÎÔÖÙÛÜŸ]',
                'keywords': ['bonjour', 'salut', 'tourisme', 'voyage', 'aidez', 'où', 'comment', 'quoi'],
                'greeting_patterns': [r'bonjour', r'salut', r'bonsoir', r'merci']
            },
            'en': {
                'keywords': ['hello', 'hi', 'tourism', 'travel', 'help', 'where', 'what', 'how', 'visit'],
                'greeting_patterns': [r'hello', r'hi', r'hey', r'good morning', r'good afternoon']
            }
        }
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect the language of input text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Tuple[str, float]: Language code and confidence score
        """
        if not text or not text.strip():
            return 'en', 0.5  # Default to English
            
        text = text.lower().strip()
        language_scores = {}
        
        # Check each supported language
        for lang_code in self.supported_languages:
            score = self._calculate_language_score(text, lang_code)
            language_scores[lang_code] = score
        
        # Find the language with highest score
        detected_lang = max(language_scores, key=language_scores.get)
        confidence = language_scores[detected_lang]
        
        # Minimum confidence threshold
        if confidence < 0.3:
            detected_lang = 'en'  # Default to English
            confidence = 0.5
        
        logger.info(f"Detected language: {detected_lang} ({self.language_names[detected_lang]}) "
                   f"with confidence: {confidence:.2f}")
        
        return detected_lang, confidence
    
    def _calculate_language_score(self, text: str, lang_code: str) -> float:
        """
        Calculate confidence score for a specific language
        
        Args:
            text (str): Input text
            lang_code (str): Language code to check
            
        Returns:
            float: Confidence score (0.0 to 1.0)
        """
        score = 0.0
        patterns = self.language_patterns.get(lang_code, {})
        
        # Unicode range check (except English)
        if 'unicode_range' in patterns:
            unicode_matches = len(re.findall(patterns['unicode_range'], text))
            if unicode_matches > 0:
                score += min(unicode_matches / len(text), 0.8)
        
        # Keyword matching
        keywords = patterns.get('keywords', [])
        keyword_matches = sum(1 for keyword in keywords if keyword in text)
        if keyword_matches > 0:
            score += min(keyword_matches / len(keywords), 0.6)
        
        # Greeting pattern matching
        greeting_patterns = patterns.get('greeting_patterns', [])
        for pattern in greeting_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.4
                break
        
        # Special handling for English (default language)
        if lang_code == 'en':
            # Boost English score if no strong indicators for other languages
            other_scores = [self._calculate_language_score(text, other_lang) 
                          for other_lang in self.supported_languages if other_lang != 'en']
            if all(s < 0.3 for s in other_scores):
                score = max(score, 0.5)
        
        return min(score, 1.0)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        
        Returns:
            Dict[str, str]: Language codes and names
        """
        return self.language_names.copy()
    
    def is_supported_language(self, lang_code: str) -> bool:
        """
        Check if a language is supported
        
        Args:
            lang_code (str): Language code to check
            
        Returns:
            bool: True if supported, False otherwise
        """
        return lang_code in self.supported_languages
    
    def get_language_info(self, lang_code: str) -> Optional[Dict[str, str]]:
        """
        Get detailed information about a language
        
        Args:
            lang_code (str): Language code
            
        Returns:
            Optional[Dict[str, str]]: Language information or None if not supported
        """
        if not self.is_supported_language(lang_code):
            return None
            
        return {
            'code': lang_code,
            'name': self.language_names[lang_code],
            'supported_features': [
                'text_processing',
                'intent_recognition',
                'response_generation',
                'cultural_context'
            ]
        }