"""
Language Detection Component

Detects the language of user input (Sinhala, Tamil, English) using
multiple detection methods for accuracy.
"""

import re
import logging
from typing import Dict, List, Tuple
from collections import Counter

try:
    from polyglot.detect import Detector
    from polyglot.detect.base import UnknownLanguage
    POLYGLOT_AVAILABLE = True
except ImportError:
    POLYGLOT_AVAILABLE = False
    logging.warning("Polyglot not available, using fallback language detection")

try:
    import fasttext
    FASTTEXT_AVAILABLE = True
except ImportError:
    FASTTEXT_AVAILABLE = False
    logging.warning("FastText not available, using fallback language detection")

logger = logging.getLogger(__name__)


class LanguageDetector:
    """
    Multilingual language detector supporting Sinhala, Tamil, and English.
    """
    
    def __init__(self):
        """Initialize the language detector."""
        self.supported_languages = {
            'en': 'English',
            'si': 'Sinhala', 
            'ta': 'Tamil'
        }
        
        # Language-specific character patterns
        self.language_patterns = {
            'si': {
                'name': 'Sinhala',
                'script': 'Sinhala',
                'char_range': (0x0D80, 0x0DFF),  # Sinhala Unicode range
                'common_chars': ['අ', 'ආ', 'ඇ', 'ඈ', 'ඉ', 'ඊ', 'උ', 'ඌ', 'ඍ', 'ඎ'],
                'keywords': ['ආයුබෝවන්', 'ස්තූතියි', 'මට', 'ඔබට', 'කොහෙද', 'කවදා']
            },
            'ta': {
                'name': 'Tamil',
                'script': 'Tamil',
                'char_range': (0x0B80, 0x0BFF),  # Tamil Unicode range
                'common_chars': ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ'],
                'keywords': ['வணக்கம்', 'நன்றி', 'எனக்கு', 'உங்களுக்கு', 'எங்கே', 'எப்போது']
            },
            'en': {
                'name': 'English',
                'script': 'Latin',
                'char_range': (0x0020, 0x007F),  # Basic Latin range
                'common_chars': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],
                'keywords': ['hello', 'thank', 'please', 'where', 'when', 'how', 'what']
            }
        }
        
        # Initialize FastText model if available
        self.fasttext_model = None
        if FASTTEXT_AVAILABLE:
            try:
                # Note: You would need to download a pre-trained model
                # self.fasttext_model = fasttext.load_model('lid.176.bin')
                pass
            except Exception as e:
                logger.warning(f"Could not load FastText model: {e}")
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Language code ('en', 'si', 'ta') or 'en' as default
        """
        if not text or not text.strip():
            return 'en'
        
        text = text.strip()
        
        # Try multiple detection methods
        detection_results = []
        
        # Method 1: Pattern-based detection
        pattern_result = self._detect_by_patterns(text)
        if pattern_result:
            detection_results.append(pattern_result)
        
        # Method 2: Polyglot detection
        if POLYGLOT_AVAILABLE:
            polyglot_result = self._detect_by_polyglot(text)
            if polyglot_result:
                detection_results.append(polyglot_result)
        
        # Method 3: FastText detection
        if self.fasttext_model:
            fasttext_result = self._detect_by_fasttext(text)
            if fasttext_result:
                detection_results.append(fasttext_result)
        
        # Method 4: Keyword-based detection
        keyword_result = self._detect_by_keywords(text)
        if keyword_result:
            detection_results.append(keyword_result)
        
        # Combine results and return most likely language
        if detection_results:
            return self._combine_detection_results(detection_results)
        
        # Default to English if no detection method worked
        return 'en'
    
    def _detect_by_patterns(self, text: str) -> Tuple[str, float]:
        """Detect language using character pattern analysis."""
        scores = {}
        
        for lang_code, lang_info in self.language_patterns.items():
            score = 0
            total_chars = 0
            
            for char in text:
                if char.isalpha():
                    total_chars += 1
                    char_code = ord(char)
                    
                    # Check if character is in language's Unicode range
                    if (lang_info['char_range'][0] <= char_code <= lang_info['char_range'][1]):
                        score += 1
                    
                    # Check if character is in common characters list
                    if char in lang_info['common_chars']:
                        score += 0.5
            
            if total_chars > 0:
                scores[lang_code] = score / total_chars
        
        if scores:
            best_lang = max(scores, key=scores.get)
            return (best_lang, scores[best_lang])
        
        return None
    
    def _detect_by_polyglot(self, text: str) -> Tuple[str, float]:
        """Detect language using Polyglot library."""
        try:
            detector = Detector(text)
            if detector.language.code in self.supported_languages:
                confidence = detector.language.confidence / 100.0
                return (detector.language.code, confidence)
        except (UnknownLanguage, Exception) as e:
            logger.debug(f"Polyglot detection failed: {e}")
        
        return None
    
    def _detect_by_fasttext(self, text: str) -> Tuple[str, float]:
        """Detect language using FastText library."""
        if not self.fasttext_model:
            return None
        
        try:
            predictions = self.fasttext_model.predict(text, k=1)
            lang_code = predictions[0][0].replace('__label__', '')
            confidence = predictions[1][0]
            
            if lang_code in self.supported_languages:
                return (lang_code, confidence)
        except Exception as e:
            logger.debug(f"FastText detection failed: {e}")
        
        return None
    
    def _detect_by_keywords(self, text: str) -> Tuple[str, float]:
        """Detect language using keyword matching."""
        text_lower = text.lower()
        scores = {}
        
        for lang_code, lang_info in self.language_patterns.items():
            score = 0
            for keyword in lang_info['keywords']:
                if keyword.lower() in text_lower:
                    score += 1
            
            if score > 0:
                scores[lang_code] = score / len(lang_info['keywords'])
        
        if scores:
            best_lang = max(scores, key=scores.get)
            return (best_lang, scores[best_lang])
        
        return None
    
    def _combine_detection_results(self, results: List[Tuple[str, float]]) -> str:
        """
        Combine multiple detection results to get the most likely language.
        
        Args:
            results: List of (language_code, confidence) tuples
            
        Returns:
            Most likely language code
        """
        if not results:
            return 'en'
        
        # Count occurrences of each language
        lang_counts = Counter(result[0] for result in results)
        
        # If one language appears more than others, use it
        if len(lang_counts) == 1:
            return list(lang_counts.keys())[0]
        
        # If multiple languages, use the one with highest average confidence
        lang_confidences = {}
        for lang_code, confidence in results:
            if lang_code not in lang_confidences:
                lang_confidences[lang_code] = []
            lang_confidences[lang_code].append(confidence)
        
        # Calculate average confidence for each language
        avg_confidences = {
            lang: sum(confs) / len(confs) 
            for lang, confs in lang_confidences.items()
        }
        
        # Return language with highest average confidence
        best_lang = max(avg_confidences, key=avg_confidences.get)
        return best_lang
    
    def get_language_name(self, lang_code: str) -> str:
        """Get the full name of a language code."""
        return self.supported_languages.get(lang_code, 'Unknown')
    
    def is_supported_language(self, lang_code: str) -> bool:
        """Check if a language code is supported."""
        return lang_code in self.supported_languages
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported language codes and names."""
        return self.supported_languages.copy()
    
    def get_detection_stats(self, text: str) -> Dict:
        """Get detailed detection statistics for debugging."""
        stats = {
            'text_length': len(text),
            'detection_methods': [],
            'pattern_scores': {},
            'keyword_matches': {},
            'final_result': None
        }
        
        # Pattern detection stats
        pattern_result = self._detect_by_patterns(text)
        if pattern_result:
            stats['detection_methods'].append('pattern')
            stats['pattern_scores'] = {
                lang: self._get_pattern_score(text, lang) 
                for lang in self.supported_languages
            }
        
        # Keyword detection stats
        for lang_code, lang_info in self.language_patterns.items():
            matches = []
            for keyword in lang_info['keywords']:
                if keyword.lower() in text.lower():
                    matches.append(keyword)
            stats['keyword_matches'][lang_code] = matches
        
        # Final result
        stats['final_result'] = self.detect_language(text)
        
        return stats
    
    def _get_pattern_score(self, text: str, lang_code: str) -> float:
        """Get pattern detection score for a specific language."""
        if lang_code not in self.language_patterns:
            return 0.0
        
        lang_info = self.language_patterns[lang_code]
        score = 0
        total_chars = 0
        
        for char in text:
            if char.isalpha():
                total_chars += 1
                char_code = ord(char)
                
                if (lang_info['char_range'][0] <= char_code <= lang_info['char_range'][1]):
                    score += 1
        
        return score / total_chars if total_chars > 0 else 0.0