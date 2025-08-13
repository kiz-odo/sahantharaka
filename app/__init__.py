from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import redis
from pymongo import MongoClient
import logging
import os
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
redis_client = None
mongo_client = None

def create_app(config_name='default'):
    """Application factory function"""
    
    app = Flask(__name__)
    
    # Load configuration
    from config import Config
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Initialize Redis (optional)
    global redis_client
    try:
        redis_client = redis.from_url(app.config.get('REDIS_URL', 'redis://localhost:6379'))
    except Exception:
        redis_client = None
        app.logger.warning("Redis connection failed - continuing without Redis")
    
    # Initialize MongoDB (optional)
    global mongo_client
    try:
        mongo_client = MongoClient(app.config.get('MONGODB_URI', 'mongodb://localhost:27017/tourism_data'))
    except Exception:
        mongo_client = None
        app.logger.warning("MongoDB connection failed - continuing without MongoDB")
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create database tables (in development)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning(f"Database initialization failed: {e}")
    
    return app

def setup_logging(app):
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    log_file = app.config.get('LOG_FILE')
    if log_file:
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    # Configure logging
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        handlers=[
            logging.FileHandler(log_file) if log_file else logging.NullHandler(),
            logging.StreamHandler()
        ]
    )
    
    app.logger.info('Tourism Dashboard startup')

def register_blueprints(app):
    """Register Flask blueprints"""
    
    from app.dashboard import dashboard_bp
    from app.api import api_bp
    from app.api.chatbot_routes import chatbot_bp
    
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp)
    
    # Add route for chatbot demo
    @app.route('/chatbot_demo.html')
    def chatbot_demo():
        from flask import send_from_directory
        return send_from_directory('.', 'chatbot_demo.html')

# Import models to ensure they are registered with SQLAlchemy
from app.models import tourist_data, accommodation, sentiment, revenue