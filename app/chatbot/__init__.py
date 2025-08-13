"""
Sri Lanka Tourism Multilingual Chatbot Package

This package provides a comprehensive multilingual chatbot solution for Sri Lanka tourism,
supporting Sinhala, Tamil, and English languages with tourism-specific knowledge.
"""

from .bot import TourismChatbot
from .language_detector import LanguageDetector
from .tourism_knowledge import TourismKnowledgeBase

__version__ = "1.0.0"
__author__ = "Sri Lanka Tourism Team"

__all__ = [
    "TourismChatbot",
    "LanguageDetector", 
    "TourismKnowledgeBase"
]