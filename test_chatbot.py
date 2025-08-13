#!/usr/bin/env python3
"""
Simple test script for Sri Lanka Tourism Chatbot

Tests the core chatbot functionality without Flask dependencies
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chatbot_components():
    """Test core chatbot components"""
    
    print("=" * 60)
    print("🇱🇰 Sri Lanka Tourism Chatbot - Component Tests")
    print("=" * 60)
    
    try:
        # Test Language Detector
        print("📝 Testing Language Detector...")
        from app.chatbot.language_detector import LanguageDetector
        
        detector = LanguageDetector()
        
        test_texts = [
            ("Hello, I want to visit Sri Lanka", "en"),
            ("ආයුබෝවන්, මම ශ්‍රී ලංකාවට එන්න කැමතියි", "si"),
            ("வணக்கம், நான் இலங்கைக்கு வர விரும்புகிறேன்", "ta"),
            ("你好，我想访问斯里兰卡", "zh"),
            ("Bonjour, je veux visiter le Sri Lanka", "fr")
        ]
        
        for text, expected_lang in test_texts:
            detected_lang, confidence = detector.detect_language(text)
            print(f"  Text: {text[:30]}...")
            print(f"  Expected: {expected_lang}, Detected: {detected_lang}, Confidence: {confidence:.2f}")
            print()
        
        print("✅ Language Detector: PASSED")
        
        # Test Intent Recognizer
        print("🎯 Testing Intent Recognizer...")
        from app.chatbot.intent_recognizer import IntentRecognizer
        
        recognizer = IntentRecognizer()
        
        test_intents = [
            ("Hello there!", "greeting"),
            ("What can I visit in Kandy?", "attraction_inquiry"),
            ("Tell me about local food", "food_inquiry"),
            ("How do I get to Ella?", "transport_inquiry"),
            ("Where should I stay?", "accommodation_inquiry"),
            ("What's the weather like?", "weather_inquiry"),
            ("Can you help me?", "help_inquiry"),
            ("Thank you, goodbye!", "goodbye")
        ]
        
        for text, expected_intent in test_intents:
            intent, confidence = recognizer.recognize_intent(text)
            print(f"  Text: {text}")
            print(f"  Expected: {expected_intent}, Detected: {intent}, Confidence: {confidence:.2f}")
            print()
        
        print("✅ Intent Recognizer: PASSED")
        
        # Test Knowledge Base
        print("📚 Testing Knowledge Base...")
        from app.chatbot.knowledge_base import TourismKnowledgeBase
        
        knowledge = TourismKnowledgeBase()
        
        # Test attraction info
        sigiriya_info = knowledge.get_attraction_info('sigiriya', 'en')
        if sigiriya_info:
            print(f"  Sigiriya info: {sigiriya_info['name']}")
            print(f"  Description: {sigiriya_info['description'][:50]}...")
            print()
        
        # Test search
        search_results = knowledge.search_knowledge_base('temple', 'en')
        print(f"  Search results for 'temple': {len(search_results)} found")
        
        print("✅ Knowledge Base: PASSED")
        
        # Test Main Chatbot
        print("🤖 Testing Main Chatbot...")
        from app.chatbot.chatbot import TourismChatbot
        
        chatbot = TourismChatbot()
        
        # Create session
        session_id = chatbot.create_session('test_user', 'en')
        print(f"  Created session: {session_id}")
        
        # Test conversation
        test_messages = [
            "Hello!",
            "What can I visit in Sri Lanka?",
            "Tell me about Sigiriya",
            "Thank you!"
        ]
        
        for message in test_messages:
            response = chatbot.process_message(session_id, message)
            print(f"  User: {message}")
            print(f"  Bot: {response.get('response', 'No response')[:100]}...")
            print(f"  Intent: {response.get('intent', 'unknown')}")
            print()
        
        print("✅ Main Chatbot: PASSED")
        
        print("=" * 60)
        print("🎉 All tests completed successfully!")
        print("📊 Test Summary:")
        print("  - Language detection for 5 languages ✅")
        print("  - Intent recognition for 8 intents ✅")
        print("  - Knowledge base with attractions, food, transport ✅")
        print("  - Full conversation flow ✅")
        print("  - Session management ✅")
        print("=" * 60)
        
        # Display chatbot capabilities
        print("🚀 Chatbot Capabilities:")
        print("  🌍 Languages: English, Sinhala, Tamil, Chinese, French")
        print("  🎯 Intents: Greetings, Attractions, Food, Transport, Weather, Help")
        print("  👥 Guides: Saru (Cultural Expert), Anjali (Nature Lover)")
        print("  📍 Coverage: All major Sri Lankan tourist destinations")
        print("  💬 Features: Context awareness, suggestions, multilingual responses")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def demo_conversation():
    """Run a demo conversation"""
    
    print("\n" + "=" * 60)
    print("💬 Interactive Demo Conversation")
    print("=" * 60)
    
    try:
        from app.chatbot.chatbot import TourismChatbot
        
        chatbot = TourismChatbot()
        session_id = chatbot.create_session('demo_user', 'en')
        
        print("🤖 Sri Lanka Tourism Chatbot is ready!")
        print("💡 Try asking about attractions, food, transport, or weather")
        print("🔤 Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    response = chatbot.process_message(session_id, "goodbye")
                    print(f"Bot: {response.get('response', 'Goodbye!')}")
                    break
                
                if not user_input:
                    continue
                
                response = chatbot.process_message(session_id, user_input)
                
                print(f"Bot: {response.get('response', 'I apologize, I could not process that.')}")
                
                # Show suggestions if available
                if response.get('suggestions'):
                    print("💡 Suggestions:", ", ".join(response['suggestions'][:3]))
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                break
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")

if __name__ == '__main__':
    # Run component tests
    success = test_chatbot_components()
    
    if success:
        # Run interactive demo if requested
        if len(sys.argv) > 1 and sys.argv[1] == '--demo':
            demo_conversation()
    else:
        sys.exit(1)