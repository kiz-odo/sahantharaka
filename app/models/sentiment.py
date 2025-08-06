from app import db
from datetime import datetime
import json

class SocialMediaPost(db.Model):
    """Model for social media posts"""
    
    __tablename__ = 'social_media_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Post identification
    post_id = db.Column(db.String(100), unique=True, index=True)  # Original post ID from platform
    platform = db.Column(db.String(20), nullable=False)  # Twitter, Instagram, Facebook, etc.
    author_id = db.Column(db.String(100), index=True)
    author_name = db.Column(db.String(200))
    author_followers = db.Column(db.Integer, default=0)
    
    # Content
    text_content = db.Column(db.Text)
    hashtags = db.Column(db.Text)  # JSON string of hashtags
    mentions = db.Column(db.Text)  # JSON string of mentions
    urls = db.Column(db.Text)  # JSON string of URLs
    
    # Engagement metrics
    likes_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    # Location and context
    location = db.Column(db.String(200))
    language = db.Column(db.String(10))  # ISO language code
    is_retweet = db.Column(db.Boolean, default=False)
    is_reply = db.Column(db.Boolean, default=False)
    
    # Tourism relevance
    is_tourism_related = db.Column(db.Boolean, default=False)
    mentioned_destinations = db.Column(db.Text)  # JSON string of destinations
    mentioned_hotels = db.Column(db.Text)  # JSON string of hotels
    
    # Timestamps
    posted_at = db.Column(db.DateTime, nullable=False, index=True)
    collected_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_hashtags(self):
        """Get hashtags as list"""
        if self.hashtags:
            try:
                return json.loads(self.hashtags)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_hashtags(self, hashtags_list):
        """Set hashtags from list"""
        self.hashtags = json.dumps(hashtags_list)
    
    def get_mentions(self):
        """Get mentions as list"""
        if self.mentions:
            try:
                return json.loads(self.mentions)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_mentions(self, mentions_list):
        """Set mentions from list"""
        self.mentions = json.dumps(mentions_list)
    
    def get_urls(self):
        """Get URLs as list"""
        if self.urls:
            try:
                return json.loads(self.urls)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_urls(self, urls_list):
        """Set URLs from list"""
        self.urls = json.dumps(urls_list)
    
    def get_mentioned_destinations(self):
        """Get mentioned destinations as list"""
        if self.mentioned_destinations:
            try:
                return json.loads(self.mentioned_destinations)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_mentioned_destinations(self, destinations_list):
        """Set mentioned destinations from list"""
        self.mentioned_destinations = json.dumps(destinations_list)
    
    def get_mentioned_hotels(self):
        """Get mentioned hotels as list"""
        if self.mentioned_hotels:
            try:
                return json.loads(self.mentioned_hotels)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_mentioned_hotels(self, hotels_list):
        """Set mentioned hotels from list"""
        self.mentioned_hotels = json.dumps(hotels_list)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'platform': self.platform,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'author_followers': self.author_followers,
            'text_content': self.text_content,
            'hashtags': self.get_hashtags(),
            'mentions': self.get_mentions(),
            'urls': self.get_urls(),
            'likes_count': self.likes_count,
            'shares_count': self.shares_count,
            'comments_count': self.comments_count,
            'views_count': self.views_count,
            'location': self.location,
            'language': self.language,
            'is_retweet': self.is_retweet,
            'is_reply': self.is_reply,
            'is_tourism_related': self.is_tourism_related,
            'mentioned_destinations': self.get_mentioned_destinations(),
            'mentioned_hotels': self.get_mentioned_hotels(),
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'collected_at': self.collected_at.isoformat() if self.collected_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SocialMediaPost {self.platform}: {self.author_name} - {self.posted_at}>'

class SentimentAnalysis(db.Model):
    """Model for sentiment analysis results"""
    
    __tablename__ = 'sentiment_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('social_media_posts.id'), nullable=False)
    post = db.relationship('SocialMediaPost', backref='sentiment_analyses')
    
    # Sentiment scores
    positive_score = db.Column(db.Float, nullable=False, default=0.0)
    negative_score = db.Column(db.Float, nullable=False, default=0.0)
    neutral_score = db.Column(db.Float, nullable=False, default=0.0)
    
    # Overall sentiment
    sentiment_label = db.Column(db.String(20), nullable=False)  # positive, negative, neutral
    confidence_score = db.Column(db.Float, default=0.0)
    
    # Detailed analysis
    emotions = db.Column(db.Text)  # JSON string of emotions (joy, sadness, anger, etc.)
    keywords = db.Column(db.Text)  # JSON string of important keywords
    topics = db.Column(db.Text)  # JSON string of identified topics
    
    # Language and processing info
    language_detected = db.Column(db.String(10))
    processing_model = db.Column(db.String(50))  # Which model was used
    processing_version = db.Column(db.String(20))
    
    # Timestamps
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_emotions(self):
        """Get emotions as dictionary"""
        if self.emotions:
            try:
                return json.loads(self.emotions)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_emotions(self, emotions_dict):
        """Set emotions from dictionary"""
        self.emotions = json.dumps(emotions_dict)
    
    def get_keywords(self):
        """Get keywords as list"""
        if self.keywords:
            try:
                return json.loads(self.keywords)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_keywords(self, keywords_list):
        """Set keywords from list"""
        self.keywords = json.dumps(keywords_list)
    
    def get_topics(self):
        """Get topics as list"""
        if self.topics:
            try:
                return json.loads(self.topics)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_topics(self, topics_list):
        """Set topics from list"""
        self.topics = json.dumps(topics_list)
    
    def calculate_sentiment_label(self):
        """Calculate sentiment label based on scores"""
        scores = {
            'positive': self.positive_score,
            'negative': self.negative_score,
            'neutral': self.neutral_score
        }
        self.sentiment_label = max(scores, key=scores.get)
        self.confidence_score = scores[self.sentiment_label]
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'positive_score': self.positive_score,
            'negative_score': self.negative_score,
            'neutral_score': self.neutral_score,
            'sentiment_label': self.sentiment_label,
            'confidence_score': self.confidence_score,
            'emotions': self.get_emotions(),
            'keywords': self.get_keywords(),
            'topics': self.get_topics(),
            'language_detected': self.language_detected,
            'processing_model': self.processing_model,
            'processing_version': self.processing_version,
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SentimentAnalysis {self.sentiment_label} (confidence: {self.confidence_score:.2f})>'