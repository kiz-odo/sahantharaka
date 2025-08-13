#!/usr/bin/env python3
"""
Run script for Sri Lanka Tourism Analytics Dashboard with Chatbot

This script starts the Flask application with the tourism analytics dashboard
and the multilingual tourism chatbot.
"""

import os
import sys
from flask import Flask
from app import create_app

def main():
    """Main entry point for the application"""
    
    # Set configuration based on environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask application
    app = create_app()
    
    # Configure application settings
    app.config['DEBUG'] = config_name == 'development'
    
    # Print startup information
    print("=" * 60)
    print("🇱🇰 Sri Lanka Tourism Analytics Dashboard & Chatbot")
    print("=" * 60)
    print(f"Environment: {config_name}")
    print(f"Debug mode: {app.config['DEBUG']}")
    print("Features:")
    print("  📊 Tourism Analytics Dashboard")
    print("  🤖 Multilingual Tourism Chatbot")
    print("  🗣️  5 Language Support (EN, SI, TA, ZH, FR)")
    print("  👥 Virtual Tour Guides")
    print("  📱 RESTful API Endpoints")
    print("=" * 60)
    print(f"Server will start at: http://localhost:5000")
    print(f"Chatbot Demo: http://localhost:5000/chatbot_demo.html")
    print(f"API Health Check: http://localhost:5000/api/chatbot/health")
    print("=" * 60)
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    try:
        # Start the Flask development server
        app.run(
            host=host,
            port=port,
            debug=app.config['DEBUG'],
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()