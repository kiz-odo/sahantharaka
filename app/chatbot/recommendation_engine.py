"""
AI-Powered Recommendation Engine

Provides intelligent, personalized recommendations for attractions, activities,
restaurants, and cultural experiences based on user preferences and behavior.
"""

import logging
import json
import random
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)


class RecommendationType(Enum):
    """Types of recommendations."""
    ATTRACTION = "attraction"
    RESTAURANT = "restaurant"
    ACTIVITY = "activity"
    CULTURAL = "cultural"
    TRANSPORT = "transport"
    ACCOMMODATION = "accommodation"
    WEATHER_BASED = "weather_based"
    CROWD_BASED = "crowd_based"


class UserPreference(Enum):
    """User preference categories."""
    HISTORY = "history"
    NATURE = "nature"
    CULTURE = "culture"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    FOOD = "food"
    PHOTOGRAPHY = "photography"
    FAMILY = "family"
    BUDGET = "budget"
    LUXURY = "luxury"


@dataclass
class Recommendation:
    """Recommendation structure."""
    id: str
    type: RecommendationType
    title: str
    title_si: str
    title_ta: str
    description: str
    description_si: str
    description_ta: str
    confidence: float
    reasoning: str
    location: str
    coordinates: Tuple[float, float]
    price_range: str
    duration: str
    best_time: str
    crowd_level: str
    weather_dependent: bool
    tags: List[str]
    user_preferences: List[UserPreference]
    image_url: Optional[str] = None


@dataclass
class UserProfile:
    """User profile for personalization."""
    user_id: str
    preferences: Dict[UserPreference, float]
    visited_places: List[str]
    interaction_history: List[Dict[str, Any]]
    language_preference: str
    budget_range: str
    travel_style: str
    created_at: datetime
    last_updated: datetime


class AIRecommendationEngine:
    """
    AI-powered recommendation engine that provides personalized suggestions
    based on user preferences, behavior, and contextual information.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the recommendation engine.
        
        Args:
            config: Configuration dictionary for recommendation settings
        """
        self.config = config or {}
        self.user_profiles = {}
        self.recommendation_database = self._initialize_recommendations()
        self.interaction_patterns = defaultdict(list)
        self.weather_data = {}
        self.crowd_data = {}
        
        # Recommendation weights
        self.weights = {
            'preference_match': 0.4,
            'context_relevance': 0.3,
            'popularity': 0.2,
            'diversity': 0.1
        }
        
        logger.info("AI Recommendation Engine initialized successfully")
    
    def _initialize_recommendations(self) -> Dict[str, Recommendation]:
        """Initialize the recommendation database."""
        recommendations = {}
        
        # Historical Attractions
        recommendations['sigiriya'] = Recommendation(
            id='sigiriya',
            type=RecommendationType.ATTRACTION,
            title='Sigiriya Rock Fortress',
            title_si='සීගිරිය ගල් බලකොටුව',
            title_ta='சிகிரியா பாறை கோட்டை',
            description='Ancient palace and fortress complex with stunning views',
            description_si='අතිශයින් ආකර්ෂණීය දර්ශන සහිත පුරාණ රාජ මාලිගාවක් සහ බලකොටුවක්',
            description_ta='அழகான காட்சிகளுடன் பழைய அரண்மனை மற்றும் கோட்டை வளாகம்',
            confidence=0.95,
            reasoning='High historical significance and architectural marvel',
            location='Central Province',
            coordinates=(7.9570, 80.7603),
            price_range='$$',
            duration='3-4 hours',
            best_time='Early morning (6-9 AM)',
            crowd_level='High',
            weather_dependent=True,
            tags=['ancient', 'fortress', 'palace', 'views', 'UNESCO'],
            user_preferences=[UserPreference.HISTORY, UserPreference.ADVENTURE, UserPreference.PHOTOGRAPHY]
        )
        
        recommendations['kandy_temple'] = Recommendation(
            id='kandy_temple',
            type=RecommendationType.CULTURAL,
            title='Temple of the Sacred Tooth Relic',
            title_si='ශ්‍රී දන්ත ධාතුන් වහන්සේගේ දේවාලය',
            title_ta='தந்தம் கோவில்',
            description='Sacred Buddhist temple housing the tooth relic of Buddha',
            description_si='බුදුන් වහන්සේගේ දන්ත ධාතුන් වහන්සේ තබා ඇති පූජනීය බෞද්ධ දේවාලයක්',
            description_ta='புத்தரின் தந்தம் துண்டத்தை வைத்திருக்கும் புனித புத்த கோவில்',
            confidence=0.92,
            reasoning='Major religious site and cultural landmark',
            location='Kandy, Central Province',
            coordinates=(7.2935, 80.6384),
            price_range='Free',
            duration='1-2 hours',
            best_time='Evening (6-8 PM)',
            crowd_level='Medium',
            weather_dependent=False,
            tags=['buddhist', 'temple', 'sacred', 'cultural', 'religious'],
            user_preferences=[UserPreference.CULTURE, UserPreference.HISTORY, UserPreference.RELAXATION]
        )
        
        recommendations['ella_rock'] = Recommendation(
            id='ella_rock',
            type=RecommendationType.ACTIVITY,
            title='Ella Rock Hiking',
            title_si='එල්ලා ගල හයිකිං',
            title_ta='எல்லா பாறை ஹைக்கிங்',
            description='Scenic mountain hiking with breathtaking views of tea plantations',
            description_si='තේ වතු සඳහා අතිශයින් ආකර්ෂණීය දර්ශන සහිත සුන්දර කඳු හයිකිං',
            description_ta='தேயிலை தோட்டங்களின் அழகான காட்சிகளுடன் மலை ஹைக்கிங்',
            confidence=0.88,
            reasoning='Popular adventure activity with stunning natural views',
            location='Ella, Uva Province',
            coordinates=(6.8667, 81.0500),
            price_range='$',
            duration='4-5 hours',
            best_time='Early morning (6-10 AM)',
            crowd_level='Medium',
            weather_dependent=True,
            tags=['hiking', 'nature', 'views', 'adventure', 'tea'],
            user_preferences=[UserPreference.ADVENTURE, UserPreference.NATURE, UserPreference.PHOTOGRAPHY]
        )
        
        recommendations['mirissa_beach'] = Recommendation(
            id='mirissa_beach',
            type=RecommendationType.ACTIVITY,
            title='Mirissa Beach & Whale Watching',
            title_si='මිරිස්ස වෙරළ සහ තල්මසුන් නැරඹීම',
            title_ta='மிரிசா கடற்கரை மற்றும் திமிங்கலங்களைப் பார்த்தல்',
            description='Beautiful beach known for whale watching and pristine coastline',
            description_si='තල්මසුන් නැරඹීමට සහ පිරිසිදු වෙරළ තීරයට ප්‍රසිද්ධ සුන්දර වෙරළ',
            description_ta='திமிங்கலங்களைப் பார்க்க மற்றும் தூய கடற்கரைக்கு பிரபலமான அழகான கடற்கரை',
            confidence=0.85,
            reasoning='Unique wildlife experience and beautiful beach',
            location='Mirissa, Southern Province',
            coordinates=(5.9435, 80.4584),
            price_range='$$',
            duration='Full day',
            best_time='December to April (whale season)',
            crowd_level='Low',
            weather_dependent=True,
            tags=['beach', 'whale watching', 'nature', 'wildlife', 'relaxation'],
            user_preferences=[UserPreference.NATURE, UserPreference.RELAXATION, UserPreference.FAMILY]
        )
        
        recommendations['rice_curry'] = Recommendation(
            id='rice_curry',
            type=RecommendationType.RESTAURANT,
            title='Traditional Rice and Curry',
            title_si='සම්ප්‍රදායික බත් සහ කරවල',
            title_ta='பாரம்பரிய அரிசி மற்றும் கறி',
            description='Authentic Sri Lankan rice and curry experience',
            description_si='සැබෑ ශ්‍රී ලාංකික බත් සහ කරවල අත්දැකීම',
            description_ta='உண்மையான இலங்கை அரிசி மற்றும் கறி அனுபவம்',
            confidence=0.90,
            reasoning='National dish and cultural culinary experience',
            location='Various locations',
            coordinates=(0.0, 0.0),
            price_range='$',
            duration='1-2 hours',
            best_time='Lunch (12-2 PM)',
            crowd_level='High',
            weather_dependent=False,
            tags=['traditional', 'local', 'authentic', 'cultural', 'budget'],
            user_preferences=[UserPreference.FOOD, UserPreference.CULTURE, UserPreference.BUDGET]
        )
        
        return recommendations
    
    def get_personalized_recommendations(self, user_id: str, 
                                       context: Dict[str, Any] = None,
                                       limit: int = 5) -> List[Recommendation]:
        """
        Get personalized recommendations for a user.
        
        Args:
            user_id: User identifier
            context: Contextual information (weather, location, time, etc.)
            limit: Maximum number of recommendations
            
        Returns:
            List of personalized recommendations
        """
        try:
            # Get or create user profile
            user_profile = self._get_or_create_user_profile(user_id)
            
            # Get context information
            context = context or {}
            weather = context.get('weather', {})
            location = context.get('location', '')
            time_of_day = context.get('time_of_day', '')
            budget = context.get('budget', '')
            
            # Calculate recommendation scores
            scored_recommendations = []
            
            for rec_id, recommendation in self.recommendation_database.items():
                score = self._calculate_recommendation_score(
                    recommendation, user_profile, context
                )
                
                scored_recommendations.append((recommendation, score))
            
            # Sort by score and apply diversity
            scored_recommendations.sort(key=lambda x: x[1], reverse=True)
            
            # Apply diversity filter to avoid similar recommendations
            diverse_recommendations = self._apply_diversity_filter(
                scored_recommendations, limit
            )
            
            # Update user profile with interaction
            self._update_user_interaction(user_id, 'recommendations_viewed', {
                'recommendations': [rec.id for rec, _ in diverse_recommendations],
                'context': context,
                'timestamp': datetime.now()
            })
            
            return [rec for rec, _ in diverse_recommendations]
            
        except Exception as e:
            logger.error(f"Error getting personalized recommendations: {str(e)}")
            return self._get_fallback_recommendations(limit)
    
    def _calculate_recommendation_score(self, recommendation: Recommendation,
                                      user_profile: UserProfile,
                                      context: Dict[str, Any]) -> float:
        """Calculate personalized score for a recommendation."""
        try:
            score = 0.0
            
            # 1. Preference matching (40% weight)
            preference_score = self._calculate_preference_score(recommendation, user_profile)
            score += preference_score * self.weights['preference_match']
            
            # 2. Context relevance (30% weight)
            context_score = self._calculate_context_score(recommendation, context)
            score += context_score * self.weights['context_relevance']
            
            # 3. Popularity (20% weight)
            popularity_score = self._calculate_popularity_score(recommendation)
            score += popularity_score * self.weights['popularity']
            
            # 4. Diversity (10% weight)
            diversity_score = self._calculate_diversity_score(recommendation, user_profile)
            score += diversity_score * self.weights['diversity']
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating recommendation score: {str(e)}")
            return 0.0
    
    def _calculate_preference_score(self, recommendation: Recommendation,
                                  user_profile: UserProfile) -> float:
        """Calculate score based on user preferences."""
        try:
            if not user_profile.preferences:
                return 0.5  # Neutral score for new users
            
            total_score = 0.0
            total_weight = 0.0
            
            for pref, weight in user_profile.preferences.items():
                if pref in recommendation.user_preferences:
                    total_score += weight
                total_weight += weight
            
            if total_weight > 0:
                return total_score / total_weight
            return 0.5
            
        except Exception:
            return 0.5
    
    def _calculate_context_score(self, recommendation: Recommendation,
                               context: Dict[str, Any]) -> float:
        """Calculate score based on contextual information."""
        try:
            score = 0.5  # Base score
            
            # Weather considerations
            weather = context.get('weather', {})
            if weather and recommendation.weather_dependent:
                weather_condition = weather.get('condition', 'unknown')
                if weather_condition in ['sunny', 'partly_cloudy']:
                    score += 0.2
                elif weather_condition in ['rainy', 'stormy']:
                    score -= 0.3
            
            # Time of day considerations
            time_of_day = context.get('time_of_day', '')
            if time_of_day and recommendation.best_time:
                if self._is_time_optimal(time_of_day, recommendation.best_time):
                    score += 0.2
            
            # Location proximity
            user_location = context.get('location', '')
            if user_location and recommendation.location:
                distance_score = self._calculate_location_score(user_location, recommendation.location)
                score += distance_score
            
            # Budget considerations
            user_budget = context.get('budget', '')
            if user_budget and recommendation.price_range:
                budget_score = self._calculate_budget_score(user_budget, recommendation.price_range)
                score += budget_score
            
            return max(0.0, min(1.0, score))
            
        except Exception:
            return 0.5
    
    def _calculate_popularity_score(self, recommendation: Recommendation) -> float:
        """Calculate popularity score based on various factors."""
        try:
            # Base popularity from crowd level
            crowd_scores = {
                'Low': 0.3,
                'Medium': 0.7,
                'High': 0.9
            }
            
            base_score = crowd_scores.get(recommendation.crowd_level, 0.5)
            
            # Adjust based on type
            type_weights = {
                RecommendationType.ATTRACTION: 1.0,
                RecommendationType.CULTURAL: 0.9,
                RecommendationType.ACTIVITY: 0.8,
                RecommendationType.RESTAURANT: 0.7
            }
            
            type_score = type_weights.get(recommendation.type, 0.5)
            
            return (base_score + type_score) / 2
            
        except Exception:
            return 0.5
    
    def _calculate_diversity_score(self, recommendation: Recommendation,
                                 user_profile: UserProfile) -> float:
        """Calculate diversity score to avoid similar recommendations."""
        try:
            # Check if user has recently visited similar places
            recent_visits = user_profile.visited_places[-5:]  # Last 5 visits
            
            if not recent_visits:
                return 1.0  # High diversity for new users
            
            # Calculate similarity with recent visits
            similarity_scores = []
            for visited_id in recent_visits:
                if visited_id in self.recommendation_database:
                    visited_rec = self.recommendation_database[visited_id]
                    similarity = self._calculate_similarity(recommendation, visited_rec)
                    similarity_scores.append(similarity)
            
            if similarity_scores:
                avg_similarity = np.mean(similarity_scores)
                return 1.0 - avg_similarity  # Higher diversity for less similar items
            
            return 0.5
            
        except Exception:
            return 0.5
    
    def _calculate_similarity(self, rec1: Recommendation, rec2: Recommendation) -> float:
        """Calculate similarity between two recommendations."""
        try:
            # Type similarity
            type_similarity = 1.0 if rec1.type == rec2.type else 0.0
            
            # Preference similarity
            pref_overlap = len(set(rec1.user_preferences) & set(rec2.user_preferences))
            pref_total = len(set(rec1.user_preferences) | set(rec2.user_preferences))
            pref_similarity = pref_overlap / pref_total if pref_total > 0 else 0.0
            
            # Tag similarity
            tag_overlap = len(set(rec1.tags) & set(rec2.tags))
            tag_total = len(set(rec1.tags) | set(rec2.tags))
            tag_similarity = tag_overlap / tag_total if tag_total > 0 else 0.0
            
            # Weighted average
            similarity = (type_similarity * 0.4 + pref_similarity * 0.3 + tag_similarity * 0.3)
            
            return similarity
            
        except Exception:
            return 0.0
    
    def _apply_diversity_filter(self, scored_recommendations: List[Tuple[Recommendation, float]],
                               limit: int) -> List[Recommendation]:
        """Apply diversity filter to avoid similar recommendations."""
        try:
            if len(scored_recommendations) <= limit:
                return [rec for rec, _ in scored_recommendations]
            
            selected = []
            remaining = scored_recommendations.copy()
            
            # Always include the top recommendation
            if remaining:
                selected.append(remaining[0][0])
                remaining.pop(0)
            
            # Select diverse recommendations
            while len(selected) < limit and remaining:
                best_diverse = None
                best_score = -1
                
                for i, (rec, score) in enumerate(remaining):
                    # Calculate diversity score
                    diversity_score = 0.0
                    for selected_rec in selected:
                        similarity = self._calculate_similarity(rec, selected_rec)
                        diversity_score += (1.0 - similarity)
                    
                    if len(selected) > 0:
                        diversity_score /= len(selected)
                    
                    # Combined score (original + diversity)
                    combined_score = score * 0.7 + diversity_score * 0.3
                    
                    if combined_score > best_score:
                        best_score = combined_score
                        best_diverse = i
                
                if best_diverse is not None:
                    selected.append(remaining[best_diverse][0])
                    remaining.pop(best_diverse)
                else:
                    break
            
            return selected
            
        except Exception as e:
            logger.error(f"Error applying diversity filter: {str(e)}")
            return [rec for rec, _ in scored_recommendations[:limit]]
    
    def _get_or_create_user_profile(self, user_id: str) -> UserProfile:
        """Get existing user profile or create a new one."""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(
                user_id=user_id,
                preferences={},
                visited_places=[],
                interaction_history=[],
                language_preference='en',
                budget_range='$$',
                travel_style='balanced',
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
        
        return self.user_profiles[user_id]
    
    def update_user_preferences(self, user_id: str, 
                               preferences: Dict[UserPreference, float]):
        """Update user preferences."""
        try:
            if user_id not in self.user_profiles:
                self._get_or_create_user_profile(user_id)
            
            profile = self.user_profiles[user_id]
            profile.preferences.update(preferences)
            profile.last_updated = datetime.now()
            
            logger.info(f"Updated preferences for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error updating user preferences: {str(e)}")
    
    def record_user_interaction(self, user_id: str, 
                               interaction_type: str,
                               data: Dict[str, Any]):
        """Record user interaction for learning."""
        try:
            if user_id not in self.user_profiles:
                self._get_or_create_user_profile(user_id)
            
            profile = self.user_profiles[user_id]
            profile.interaction_history.append({
                'type': interaction_type,
                'data': data,
                'timestamp': datetime.now()
            })
            
            # Keep only last 100 interactions
            if len(profile.interaction_history) > 100:
                profile.interaction_history = profile.interaction_history[-100:]
            
            profile.last_updated = datetime.now()
            
        except Exception as e:
            logger.error(f"Error recording user interaction: {str(e)}")
    
    def _update_user_interaction(self, user_id: str, 
                                interaction_type: str,
                                data: Dict[str, Any]):
        """Internal method to update user interactions."""
        self.record_user_interaction(user_id, interaction_type, data)
    
    def _get_fallback_recommendations(self, limit: int) -> List[Recommendation]:
        """Get fallback recommendations when personalization fails."""
        try:
            # Return popular recommendations
            popular_recs = [
                self.recommendation_database['sigiriya'],
                self.recommendation_database['kandy_temple'],
                self.recommendation_database['ella_rock']
            ]
            
            return popular_recs[:limit]
            
        except Exception:
            return []
    
    def _is_time_optimal(self, current_time: str, best_time: str) -> bool:
        """Check if current time is optimal for the recommendation."""
        try:
            # Simple time matching logic
            if 'morning' in best_time.lower() and 'morning' in current_time.lower():
                return True
            elif 'evening' in best_time.lower() and 'evening' in current_time.lower():
                return True
            elif 'afternoon' in best_time.lower() and 'afternoon' in current_time.lower():
                return True
            
            return False
            
        except Exception:
            return False
    
    def _calculate_location_score(self, user_location: str, rec_location: str) -> float:
        """Calculate location proximity score."""
        try:
            # Simple location matching
            if user_location.lower() in rec_location.lower() or rec_location.lower() in user_location.lower():
                return 0.3  # Same area
            elif any(province in rec_location.lower() for province in ['central', 'southern', 'western']):
                return 0.1  # Same province
            else:
                return -0.1  # Different area
            
        except Exception:
            return 0.0
    
    def _calculate_budget_score(self, user_budget: str, rec_price_range: str) -> float:
        """Calculate budget compatibility score."""
        try:
            budget_mapping = {
                '$': 1,      # Budget
                '$$': 2,     # Mid-range
                '$$$': 3,    # High-end
                '$$$$': 4    # Luxury
            }
            
            user_budget_level = budget_mapping.get(user_budget, 2)
            rec_price_level = budget_mapping.get(rec_price_range, 2)
            
            # Prefer same or lower price level
            if rec_price_level <= user_budget_level:
                return 0.2
            else:
                return -0.3
            
        except Exception:
            return 0.0
    
    def get_recommendation_stats(self) -> Dict[str, Any]:
        """Get statistics about the recommendation engine."""
        return {
            'total_recommendations': len(self.recommendation_database),
            'total_users': len(self.user_profiles),
            'recommendation_types': {
                rec_type.value: len([r for r in self.recommendation_database.values() if r.type == rec_type])
                for rec_type in RecommendationType
            },
            'average_preferences_per_user': np.mean([
                len(profile.preferences) for profile in self.user_profiles.values()
            ]) if self.user_profiles else 0
        }