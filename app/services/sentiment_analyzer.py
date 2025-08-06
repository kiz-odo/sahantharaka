import logging
from textblob import TextBlob
import re
from datetime import datetime
from app import db
from app.models import SocialMediaPost, SentimentAnalysis
from config import Config

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Service for analyzing sentiment in social media posts"""
    
    def __init__(self):
        self.config = Config()
        
    def analyze_post_sentiment(self, post_text, language='en'):
        """Analyze sentiment of a single post"""
        try:
            # Clean text
            cleaned_text = self._clean_text(post_text)
            
            # Create TextBlob object
            blob = TextBlob(cleaned_text)
            
            # Get polarity (-1 to 1)
            polarity = blob.sentiment.polarity
            
            # Get subjectivity (0 to 1)
            subjectivity = blob.sentiment.subjectivity
            
            # Determine sentiment label
            if polarity > 0.1:
                sentiment_label = 'positive'
                positive_score = polarity
                negative_score = 0
                neutral_score = 1 - polarity
            elif polarity < -0.1:
                sentiment_label = 'negative'
                positive_score = 0
                negative_score = abs(polarity)
                neutral_score = 1 - abs(polarity)
            else:
                sentiment_label = 'neutral'
                positive_score = 0
                negative_score = 0
                neutral_score = 1
            
            # Extract keywords
            keywords = self._extract_keywords(cleaned_text)
            
            # Extract topics
            topics = self._extract_topics(cleaned_text)
            
            # Detect emotions
            emotions = self._detect_emotions(cleaned_text)
            
            return {
                'positive_score': positive_score,
                'negative_score': negative_score,
                'neutral_score': neutral_score,
                'sentiment_label': sentiment_label,
                'confidence_score': abs(polarity),
                'subjectivity': subjectivity,
                'keywords': keywords,
                'topics': topics,
                'emotions': emotions,
                'language_detected': language,
                'processing_model': 'TextBlob',
                'processing_version': '0.17.1'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return None
    
    def analyze_batch_sentiment(self, posts):
        """Analyze sentiment for multiple posts"""
        results = []
        
        for post in posts:
            try:
                sentiment_result = self.analyze_post_sentiment(
                    post.text_content, 
                    post.language or 'en'
                )
                
                if sentiment_result:
                    # Create sentiment analysis record
                    sentiment_analysis = SentimentAnalysis(
                        post_id=post.id,
                        positive_score=sentiment_result['positive_score'],
                        negative_score=sentiment_result['negative_score'],
                        neutral_score=sentiment_result['neutral_score'],
                        sentiment_label=sentiment_result['sentiment_label'],
                        confidence_score=sentiment_result['confidence_score'],
                        language_detected=sentiment_result['language_detected'],
                        processing_model=sentiment_result['processing_model'],
                        processing_version=sentiment_result['processing_version']
                    )
                    
                    # Set JSON fields
                    sentiment_analysis.set_keywords(sentiment_result['keywords'])
                    sentiment_analysis.set_topics(sentiment_result['topics'])
                    sentiment_analysis.set_emotions(sentiment_result['emotions'])
                    
                    # Calculate sentiment label
                    sentiment_analysis.calculate_sentiment_label()
                    
                    # Save to database
                    db.session.add(sentiment_analysis)
                    results.append(sentiment_analysis)
                
            except Exception as e:
                logger.error(f"Error analyzing sentiment for post {post.id}: {str(e)}")
                continue
        
        try:
            db.session.commit()
            logger.info(f"Analyzed sentiment for {len(results)} posts")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving sentiment analysis: {str(e)}")
        
        return results
    
    def get_sentiment_summary(self, start_date=None, end_date=None, platform=None):
        """Get sentiment summary statistics"""
        try:
            query = db.session.query(SentimentAnalysis).join(SocialMediaPost)
            
            if start_date:
                query = query.filter(SocialMediaPost.posted_at >= start_date)
            if end_date:
                query = query.filter(SocialMediaPost.posted_at <= end_date)
            if platform:
                query = query.filter(SocialMediaPost.platform == platform)
            
            # Get sentiment distribution
            sentiment_distribution = db.session.query(
                SentimentAnalysis.sentiment_label,
                db.func.count(SentimentAnalysis.id).label('count')
            ).join(SocialMediaPost).filter(query.whereclause).group_by(
                SentimentAnalysis.sentiment_label
            ).all()
            
            # Get average sentiment scores
            avg_scores = db.session.query(
                db.func.avg(SentimentAnalysis.positive_score).label('avg_positive'),
                db.func.avg(SentimentAnalysis.negative_score).label('avg_negative'),
                db.func.avg(SentimentAnalysis.neutral_score).label('avg_neutral'),
                db.func.avg(SentimentAnalysis.confidence_score).label('avg_confidence')
            ).join(SocialMediaPost).filter(query.whereclause).first()
            
            # Get top keywords
            # This would require more complex querying or post-processing
            
            return {
                'sentiment_distribution': {
                    item.sentiment_label: item.count 
                    for item in sentiment_distribution
                },
                'average_scores': {
                    'positive': avg_scores.avg_positive or 0,
                    'negative': avg_scores.avg_negative or 0,
                    'neutral': avg_scores.avg_neutral or 0,
                    'confidence': avg_scores.avg_confidence or 0
                },
                'total_posts': sum(item.count for item in sentiment_distribution)
            }
            
        except Exception as e:
            logger.error(f"Error getting sentiment summary: {str(e)}")
            return None
    
    def _clean_text(self, text):
        """Clean text for sentiment analysis"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtags but keep the text
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text)
        
        return text.strip()
    
    def _extract_keywords(self, text):
        """Extract keywords from text"""
        try:
            blob = TextBlob(text)
            
            # Get noun phrases and words
            keywords = []
            
            # Add noun phrases
            keywords.extend([phrase.lower() for phrase in blob.noun_phrases])
            
            # Add individual words (nouns, adjectives, verbs)
            for word, tag in blob.tags:
                if tag.startswith(('NN', 'JJ', 'VB')) and len(word) > 3:
                    keywords.append(word.lower())
            
            # Remove duplicates and limit
            keywords = list(set(keywords))[:20]
            
            return keywords
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    def _extract_topics(self, text):
        """Extract topics from text"""
        try:
            # Define tourism-related topics
            tourism_topics = {
                'accommodation': ['hotel', 'resort', 'guesthouse', 'villa', 'room', 'stay', 'accommodation'],
                'food': ['restaurant', 'food', 'cuisine', 'meal', 'dining', 'breakfast', 'lunch', 'dinner'],
                'transportation': ['transport', 'bus', 'train', 'taxi', 'car', 'airport', 'travel'],
                'attractions': ['temple', 'beach', 'museum', 'park', 'garden', 'fort', 'palace', 'ruins'],
                'activities': ['sightseeing', 'tour', 'hiking', 'swimming', 'shopping', 'spa', 'massage'],
                'culture': ['culture', 'traditional', 'heritage', 'history', 'art', 'music', 'dance'],
                'nature': ['nature', 'wildlife', 'forest', 'mountain', 'ocean', 'river', 'waterfall'],
                'weather': ['weather', 'climate', 'sunny', 'rainy', 'hot', 'cold', 'temperature']
            }
            
            text_lower = text.lower()
            detected_topics = []
            
            for topic, keywords in tourism_topics.items():
                if any(keyword in text_lower for keyword in keywords):
                    detected_topics.append(topic)
            
            return detected_topics
            
        except Exception as e:
            logger.error(f"Error extracting topics: {str(e)}")
            return []
    
    def _detect_emotions(self, text):
        """Detect emotions in text"""
        try:
            # Simple emotion detection based on keywords
            emotion_keywords = {
                'joy': ['happy', 'excited', 'amazing', 'wonderful', 'fantastic', 'great', 'love', 'enjoy'],
                'sadness': ['sad', 'disappointed', 'terrible', 'awful', 'bad', 'hate', 'dislike'],
                'anger': ['angry', 'furious', 'mad', 'annoyed', 'frustrated', 'upset'],
                'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'terrified'],
                'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'unexpected'],
                'disgust': ['disgusting', 'gross', 'nasty', 'revolting', 'sickening']
            }
            
            text_lower = text.lower()
            detected_emotions = {}
            
            for emotion, keywords in emotion_keywords.items():
                count = sum(1 for keyword in keywords if keyword in text_lower)
                if count > 0:
                    detected_emotions[emotion] = count
            
            return detected_emotions
            
        except Exception as e:
            logger.error(f"Error detecting emotions: {str(e)}")
            return {}
    
    def is_tourism_related(self, text):
        """Check if text is tourism-related"""
        try:
            tourism_keywords = [
                'sri lanka', 'colombo', 'kandy', 'galle', 'sigiriya', 'anuradhapura',
                'tourism', 'tourist', 'travel', 'vacation', 'holiday', 'trip',
                'hotel', 'resort', 'guesthouse', 'accommodation', 'booking',
                'beach', 'temple', 'culture', 'heritage', 'nature', 'wildlife',
                'food', 'cuisine', 'restaurant', 'transport', 'airport',
                'visit', 'explore', 'discover', 'experience', 'adventure'
            ]
            
            text_lower = text.lower()
            return any(keyword in text_lower for keyword in tourism_keywords)
            
        except Exception as e:
            logger.error(f"Error checking tourism relevance: {str(e)}")
            return False