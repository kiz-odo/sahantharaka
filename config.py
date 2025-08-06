import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://localhost/tourism_dashboard'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # MongoDB Configuration
    MONGODB_URI = os.environ.get('MONGODB_URL') or \
        'mongodb://localhost:27017/tourism_data'
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379'
    
    # API Keys
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    
    # Dashboard Configuration
    DASHBOARD_REFRESH_INTERVAL = int(os.environ.get('DASHBOARD_REFRESH_INTERVAL', 300))  # 5 minutes
    DATA_UPDATE_INTERVAL = int(os.environ.get('DATA_UPDATE_INTERVAL', 600))  # 10 minutes
    
    # Sentiment Analysis Configuration
    SENTIMENT_ANALYSIS_LANGUAGES = ['en', 'si', 'ta']  # English, Sinhala, Tamil
    SENTIMENT_UPDATE_INTERVAL = int(os.environ.get('SENTIMENT_UPDATE_INTERVAL', 1800))  # 30 minutes
    
    # Forecasting Configuration
    FORECAST_HORIZON_DAYS = int(os.environ.get('FORECAST_HORIZON_DAYS', 30))
    FORECAST_UPDATE_INTERVAL = int(os.environ.get('FORECAST_UPDATE_INTERVAL', 86400))  # 24 hours
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')
    
    # Security Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = REDIS_URL
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Email Configuration (for alerts)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Sri Lanka Specific Configuration
    SRI_LANKA_COORDINATES = {
        'lat': 7.8731,
        'lon': 80.7718
    }
    
    # Popular destinations in Sri Lanka
    POPULAR_DESTINATIONS = [
        'Colombo', 'Kandy', 'Galle', 'Sigiriya', 'Anuradhapura',
        'Polonnaruwa', 'Nuwara Eliya', 'Bentota', 'Mirissa', 'Ella',
        'Yala National Park', 'Udawalawe National Park', 'Dambulla',
        'Trincomalee', 'Jaffna', 'Arugam Bay', 'Hikkaduwa', 'Unawatuna'
    ]
    
    # Tourist source countries
    TOP_SOURCE_COUNTRIES = [
        'India', 'United Kingdom', 'Germany', 'France', 'Australia',
        'United States', 'China', 'Russia', 'Netherlands', 'Canada',
        'Switzerland', 'Italy', 'Japan', 'South Korea', 'Singapore',
        'Malaysia', 'Thailand', 'Maldives', 'United Arab Emirates'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://localhost/tourism_dashboard_dev'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Additional production settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tourism_dashboard_test'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}