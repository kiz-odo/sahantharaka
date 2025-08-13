"""
Sri Lanka Tourism Multilingual Chatbot Package

This package provides a comprehensive multilingual chatbot solution for Sri Lanka tourism,
supporting Sinhala, Tamil, English, Chinese, and French languages with advanced security features
and comprehensive trip planning capabilities.
"""

from .bot import TourismChatbot
from .language_detector import LanguageDetector
from .tourism_knowledge import TourismKnowledgeBase
from .security_manager import SecurityManager
from .trip_planner import TripPlanner

__version__ = "1.0.0"
__author__ = "Sri Lanka Tourism Team"

__all__ = [
    "TourismChatbot",
    "LanguageDetector", 
    "TourismKnowledgeBase",
    "SecurityManager",
    "TripPlanner"
]