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
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Initialize Redis
    global redis_client
    redis_client = redis.from_url(app.config['REDIS_URL'])
    
    # Initialize MongoDB
    global mongo_client
    mongo_client = MongoClient(app.config['MONGODB_URI'])
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

def setup_logging(app):
    """Setup application logging"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, app.config['LOG_LEVEL']),
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        handlers=[
            logging.FileHandler(app.config['LOG_FILE']),
            logging.StreamHandler()
        ]
    )
    
    app.logger.info('Tourism Dashboard startup')

def register_blueprints(app):
    """Register Flask blueprints"""
    
    from app.dashboard import dashboard_bp
    from app.api import api_bp
    
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')

# Import models to ensure they are registered with SQLAlchemy
from app.models import tourist_data, accommodation, sentiment, revenue