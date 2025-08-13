from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import chatbot routes
from .chatbot_routes import chatbot_bp

from . import routes