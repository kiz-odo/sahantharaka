"""
Trip Planning Component

Provides comprehensive trip planning functionality including itinerary creation,
budget management, booking assistance, and personalized travel recommendations.
"""

import logging
import json
import uuid
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class TripType(Enum):
    """Types of trips supported."""
    CULTURAL = "cultural"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    FAMILY = "family"
    BUDGET = "budget"
    LUXURY = "luxury"
    PHOTOGRAPHY = "photography"
    FOOD = "food"
    NATURE = "nature"
    HISTORICAL = "historical"


class BudgetLevel(Enum):
    """Budget levels for trip planning."""
    BUDGET = "budget"      # $50-100/day
    MODERATE = "moderate"  # $100-200/day
    LUXURY = "luxury"      # $200-500+/day


class Season(Enum):
    """Sri Lanka seasons for trip planning."""
    PEAK = "peak"          # December-April
    SHOULDER = "shoulder"  # May-July, September-November
    LOW = "low"            # August (monsoon)


@dataclass
class TripPreferences:
    """User trip preferences for planning."""
    trip_type: TripType
    budget_level: BudgetLevel
    duration_days: int
    group_size: int
    preferred_season: Season
    interests: List[str]
    accommodation_type: str
    transport_preference: str
    dietary_restrictions: List[str]
    accessibility_requirements: List[str]
    language_preference: str


@dataclass
class TripItinerary:
    """Complete trip itinerary."""
    trip_id: str
    user_id: str
    title: str
    preferences: TripPreferences
    start_date: datetime
    end_date: datetime
    total_budget: float
    daily_itineraries: List[Dict]
    accommodation_bookings: List[Dict]
    transport_bookings: List[Dict]
    activity_bookings: List[Dict]
    created_at: datetime
    updated_at: datetime
    status: str = "draft"


@dataclass
class DailyPlan:
    """Daily itinerary plan."""
    day_number: int
    date: datetime
    location: str
    activities: List[Dict]
    meals: List[Dict]
    accommodation: Dict
    transport: Dict
    estimated_cost: float
    weather_forecast: Dict
    cultural_notes: List[str]


class TripPlanner:
    """
    Comprehensive trip planning system for Sri Lanka tourism.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the trip planner.
        
        Args:
            config: Configuration dictionary for trip planning settings
        """
        self.config = config or {}
        
        # Trip planning data
        self.trip_templates = self._initialize_trip_templates()
        self.attraction_data = self._initialize_attraction_data()
        self.accommodation_data = self._initialize_accommodation_data()
        self.transport_data = self._initialize_transport_data()
        self.activity_data = self._initialize_activity_data()
        
        # User trip data
        self.user_trips = {}
        self.trip_recommendations = {}
        
        logger.info("Trip Planner initialized successfully")
    
    def create_trip_plan(self, user_id: str, preferences: Dict) -> Dict:
        """
        Create a personalized trip plan based on user preferences.
        
        Args:
            user_id: Unique user identifier
            preferences: User trip preferences
            
        Returns:
            Complete trip plan with itinerary
        """
        try:
            # Parse preferences
            trip_prefs = self._parse_preferences(preferences)
            
            # Generate trip plan
            trip_plan = self._generate_trip_plan(trip_prefs)
            
            # Create trip itinerary
            itinerary = self._create_itinerary(user_id, trip_prefs, trip_plan)
            
            # Store user trip
            if user_id not in self.user_trips:
                self.user_trips[user_id] = []
            
            self.user_trips[user_id].append(itinerary)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(trip_prefs)
            
            return {
                'trip_id': itinerary.trip_id,
                'itinerary': asdict(itinerary),
                'recommendations': recommendations,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error creating trip plan: {str(e)}")
            return {
                'error': 'Failed to create trip plan',
                'status': 'error'
            }
    
    def _parse_preferences(self, preferences: Dict) -> TripPreferences:
        """Parse and validate user preferences."""
        try:
            return TripPreferences(
                trip_type=TripType(preferences.get('trip_type', 'cultural')),
                budget_level=BudgetLevel(preferences.get('budget_level', 'moderate')),
                duration_days=int(preferences.get('duration_days', 7)),
                group_size=int(preferences.get('group_size', 2)),
                preferred_season=Season(preferences.get('preferred_season', 'peak')),
                interests=preferences.get('interests', []),
                accommodation_type=preferences.get('accommodation_type', 'hotel'),
                transport_preference=preferences.get('transport_preference', 'mix'),
                dietary_restrictions=preferences.get('dietary_restrictions', []),
                accessibility_requirements=preferences.get('accessibility_requirements', []),
                language_preference=preferences.get('language_preference', 'en')
            )
        except Exception as e:
            logger.error(f"Error parsing preferences: {str(e)}")
            # Return default preferences
            return TripPreferences(
                trip_type=TripType.CULTURAL,
                budget_level=BudgetLevel.MODERATE,
                duration_days=7,
                group_size=2,
                preferred_season=Season.PEAK,
                interests=['culture', 'history'],
                accommodation_type='hotel',
                transport_preference='mix',
                dietary_restrictions=[],
                accessibility_requirements=[],
                language_preference='en'
            )
    
    def _generate_trip_plan(self, preferences: TripPreferences) -> Dict:
        """Generate trip plan based on preferences."""
        try:
            # Get base template
            template = self._get_trip_template(preferences.trip_type)
            
            # Customize based on preferences
            plan = self._customize_plan(template, preferences)
            
            # Optimize route and timing
            plan = self._optimize_route(plan, preferences)
            
            # Calculate budget
            plan = self._calculate_budget(plan, preferences)
            
            return plan
            
        except Exception as e:
            logger.error(f"Error generating trip plan: {str(e)}")
            return {}
    
    def _get_trip_template(self, trip_type: TripType) -> Dict:
        """Get base trip template for the specified type."""
        return self.trip_templates.get(trip_type.value, self.trip_templates['cultural'])
    
    def _customize_plan(self, template: Dict, preferences: TripPreferences) -> Dict:
        """Customize template based on user preferences."""
        try:
            plan = template.copy()
            
            # Adjust duration
            if preferences.duration_days != len(plan['daily_plans']):
                plan['daily_plans'] = self._adjust_duration(
                    plan['daily_plans'], 
                    preferences.duration_days
                )
            
            # Adjust group size considerations
            plan = self._adjust_for_group_size(plan, preferences.group_size)
            
            # Add personal interests
            plan = self._add_personal_interests(plan, preferences.interests)
            
            # Adjust for season
            plan = self._adjust_for_season(plan, preferences.preferred_season)
            
            return plan
            
        except Exception as e:
            logger.error(f"Error customizing plan: {str(e)}")
            return template
    
    def _adjust_duration(self, daily_plans: List, target_days: int) -> List:
        """Adjust daily plans to match target duration."""
        try:
            if target_days <= len(daily_plans):
                # Reduce duration
                return daily_plans[:target_days]
            else:
                # Extend duration
                extended_plans = daily_plans.copy()
                while len(extended_plans) < target_days:
                    # Add flexible days
                    flexible_day = self._create_flexible_day(len(extended_plans) + 1)
                    extended_plans.append(flexible_day)
                return extended_plans
                
        except Exception as e:
            logger.error(f"Error adjusting duration: {str(e)}")
            return daily_plans
    
    def _create_flexible_day(self, day_number: int) -> Dict:
        """Create a flexible day plan."""
        return {
            'day_number': day_number,
            'location': 'Flexible',
            'activities': [
                {
                    'name': 'Free Time / Personal Exploration',
                    'description': 'Flexible time for personal interests',
                    'duration': '4-6 hours',
                    'cost': 0,
                    'type': 'flexible'
                }
            ],
            'meals': [
                {
                    'type': 'breakfast',
                    'suggestion': 'Local cafe or hotel breakfast',
                    'cost': 15
                },
                {
                    'type': 'lunch',
                    'suggestion': 'Explore local cuisine',
                    'cost': 20
                },
                {
                    'type': 'dinner',
                    'suggestion': 'Restaurant of choice',
                    'cost': 25
                }
            ],
            'accommodation': {
                'type': 'continue_current',
                'description': 'Continue with current accommodation'
            },
            'transport': {
                'type': 'local',
                'description': 'Local transport or walking',
                'cost': 10
            },
            'estimated_cost': 70,
            'notes': ['Flexible day for personal interests', 'Opportunity to explore local areas']
        }
    
    def _adjust_for_group_size(self, plan: Dict, group_size: int) -> Dict:
        """Adjust plan considerations for group size."""
        try:
            # Adjust accommodation recommendations
            if group_size > 4:
                plan['accommodation_notes'] = 'Consider family rooms or multiple rooms'
            elif group_size == 1:
                plan['accommodation_notes'] = 'Single rooms or hostels recommended'
            
            # Adjust transport recommendations
            if group_size > 6:
                plan['transport_notes'] = 'Private vehicle or multiple vehicles recommended'
            elif group_size <= 2:
                plan['transport_notes'] = 'Public transport or tuk-tuk suitable'
            
            # Adjust activity timing
            for day_plan in plan['daily_plans']:
                for activity in day_plan.get('activities', []):
                    if group_size > 4:
                        activity['duration'] = self._increase_duration(activity.get('duration', '2 hours'))
            
            return plan
            
        except Exception as e:
            logger.error(f"Error adjusting for group size: {str(e)}")
            return plan
    
    def _increase_duration(self, duration: str) -> str:
        """Increase activity duration for larger groups."""
        try:
            if 'hour' in duration.lower():
                # Extract number and increase by 30 minutes
                parts = duration.split()
                for i, part in enumerate(parts):
                    if part.isdigit():
                        hours = int(part)
                        if hours < 4:
                            parts[i] = str(hours + 1)
                        break
                return ' '.join(parts)
            return duration
        except Exception:
            return duration
    
    def _add_personal_interests(self, plan: Dict, interests: List[str]) -> Dict:
        """Add activities based on personal interests."""
        try:
            for day_plan in plan['daily_plans']:
                for interest in interests:
                    if interest.lower() in ['photography', 'photo']:
                        day_plan['activities'].append({
                            'name': 'Photography Opportunity',
                            'description': 'Scenic spots for photography',
                            'duration': '1 hour',
                            'cost': 0,
                            'type': 'photography'
                        })
                    elif interest.lower() in ['food', 'cuisine', 'cooking']:
                        day_plan['activities'].append({
                            'name': 'Local Food Experience',
                            'description': 'Try local specialties and street food',
                            'duration': '2 hours',
                            'cost': 25,
                            'type': 'food'
                        })
                    elif interest.lower() in ['shopping', 'market']:
                        day_plan['activities'].append({
                            'name': 'Local Market Visit',
                            'description': 'Explore local markets and shops',
                            'duration': '1.5 hours',
                            'cost': 0,
                            'type': 'shopping'
                        })
            
            return plan
            
        except Exception as e:
            logger.error(f"Error adding personal interests: {str(e)}")
            return plan
    
    def _adjust_for_season(self, plan: Dict, season: Season) -> Dict:
        """Adjust plan based on season."""
        try:
            season_notes = {
                Season.PEAK: {
                    'crowds': 'High season - book accommodations early',
                    'weather': 'Best weather - perfect for outdoor activities',
                    'prices': 'Higher prices - budget accordingly'
                },
                Season.SHOULDER: {
                    'crowds': 'Moderate crowds - good balance',
                    'weather': 'Good weather with occasional rain',
                    'prices': 'Moderate prices - good value'
                },
                Season.LOW: {
                    'crowds': 'Low season - fewer tourists',
                    'weather': 'Monsoon season - indoor activities recommended',
                    'prices': 'Lower prices - great deals available'
                }
            }
            
            plan['season_notes'] = season_notes.get(season, {})
            
            # Adjust activities for weather
            if season == Season.LOW:
                for day_plan in plan['daily_plans']:
                    # Add indoor alternatives
                    day_plan['weather_alternatives'] = [
                        'Visit museums and galleries',
                        'Indoor cultural shows',
                        'Shopping in covered markets',
                        'Spa and wellness activities'
                    ]
            
            return plan
            
        except Exception as e:
            logger.error(f"Error adjusting for season: {str(e)}")
            return plan
    
    def _optimize_route(self, plan: Dict, preferences: TripPreferences) -> Dict:
        """Optimize route for efficiency and experience."""
        try:
            # Simple route optimization
            # In production, use more sophisticated algorithms
            
            daily_plans = plan['daily_plans']
            
            # Group activities by location
            for i, day_plan in enumerate(daily_plans):
                if i > 0:
                    # Check if we can optimize location transitions
                    prev_location = daily_plans[i-1]['location']
                    current_location = day_plan['location']
                    
                    if prev_location != current_location:
                        # Add transport note
                        day_plan['transport_note'] = f"Travel from {prev_location} to {current_location}"
            
            return plan
            
        except Exception as e:
            logger.error(f"Error optimizing route: {str(e)}")
            return plan
    
    def _calculate_budget(self, plan: Dict, preferences: TripPreferences) -> Dict:
        """Calculate detailed budget breakdown."""
        try:
            total_budget = 0
            daily_budgets = []
            
            for day_plan in plan['daily_plans']:
                day_cost = 0
                
                # Activities cost
                for activity in day_plan.get('activities', []):
                    day_cost += activity.get('cost', 0)
                
                # Meals cost
                for meal in day_plan.get('meals', []):
                    day_cost += meal.get('cost', 0)
                
                # Transport cost
                day_cost += day_plan.get('transport', {}).get('cost', 0)
                
                # Accommodation cost (if specified)
                if 'accommodation' in day_plan and 'cost' in day_plan['accommodation']:
                    day_cost += day_plan['accommodation']['cost']
                
                day_plan['estimated_cost'] = day_cost
                daily_budgets.append(day_cost)
                total_budget += day_cost
            
            # Add accommodation costs if not included in daily plans
            accommodation_cost = self._calculate_accommodation_cost(preferences)
            total_budget += accommodation_cost
            
            # Add transport costs if not included in daily plans
            transport_cost = self._calculate_transport_cost(preferences)
            total_budget += transport_cost
            
            plan['budget_breakdown'] = {
                'total_budget': total_budget,
                'daily_budgets': daily_budgets,
                'accommodation_cost': accommodation_cost,
                'transport_cost': transport_cost,
                'activities_cost': sum(daily_budgets),
                'budget_per_day': total_budget / len(daily_budgets) if daily_budgets else 0
            }
            
            return plan
            
        except Exception as e:
            logger.error(f"Error calculating budget: {str(e)}")
            return plan
    
    def _calculate_accommodation_cost(self, preferences: TripPreferences) -> float:
        """Calculate accommodation costs based on preferences."""
        try:
            base_costs = {
                BudgetLevel.BUDGET: 30,
                BudgetLevel.MODERATE: 80,
                BudgetLevel.LUXURY: 200
            }
            
            base_cost = base_costs.get(preferences.budget_level, 80)
            
            # Adjust for group size
            if preferences.group_size > 2:
                base_cost *= (preferences.group_size * 0.6)  # Group discount
            
            # Adjust for accommodation type
            type_multipliers = {
                'hostel': 0.5,
                'guesthouse': 0.8,
                'hotel': 1.0,
                'resort': 1.5,
                'villa': 2.0
            }
            
            multiplier = type_multipliers.get(preferences.accommodation_type, 1.0)
            base_cost *= multiplier
            
            return base_cost * preferences.duration_days
            
        except Exception as e:
            logger.error(f"Error calculating accommodation cost: {str(e)}")
            return 80 * preferences.duration_days
    
    def _calculate_transport_cost(self, preferences: TripPreferences) -> float:
        """Calculate transport costs based on preferences."""
        try:
            base_costs = {
                BudgetLevel.BUDGET: 15,
                BudgetLevel.MODERATE: 30,
                BudgetLevel.LUXURY: 80
            }
            
            base_cost = base_costs.get(preferences.budget_level, 30)
            
            # Adjust for transport preference
            transport_multipliers = {
                'public': 0.5,
                'mix': 1.0,
                'private': 2.0
            }
            
            multiplier = transport_multipliers.get(preferences.transport_preference, 1.0)
            base_cost *= multiplier
            
            return base_cost * preferences.duration_days
            
        except Exception as e:
            logger.error(f"Error calculating transport cost: {str(e)}")
            return 30 * preferences.duration_days
    
    def _create_itinerary(self, user_id: str, preferences: TripPreferences, plan: Dict) -> TripItinerary:
        """Create complete trip itinerary."""
        try:
            trip_id = str(uuid.uuid4())
            start_date = datetime.now() + timedelta(days=30)  # Default start in 30 days
            end_date = start_date + timedelta(days=preferences.duration_days)
            
            itinerary = TripItinerary(
                trip_id=trip_id,
                user_id=user_id,
                title=f"Sri Lanka {preferences.trip_type.value.title()} Trip",
                preferences=preferences,
                start_date=start_date,
                end_date=end_date,
                total_budget=plan.get('budget_breakdown', {}).get('total_budget', 0),
                daily_itineraries=plan.get('daily_plans', []),
                accommodation_bookings=[],
                transport_bookings=[],
                activity_bookings=[],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            return itinerary
            
        except Exception as e:
            logger.error(f"Error creating itinerary: {str(e)}")
            raise
    
    def _generate_recommendations(self, preferences: TripPreferences) -> Dict:
        """Generate personalized recommendations."""
        try:
            recommendations = {
                'attractions': self._get_attraction_recommendations(preferences),
                'accommodations': self._get_accommodation_recommendations(preferences),
                'restaurants': self._get_restaurant_recommendations(preferences),
                'activities': self._get_activity_recommendations(preferences),
                'transport': self._get_transport_recommendations(preferences),
                'tips': self._get_travel_tips(preferences)
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {}
    
    def _get_attraction_recommendations(self, preferences: TripPreferences) -> List[Dict]:
        """Get attraction recommendations based on preferences."""
        try:
            # Filter attractions based on trip type and interests
            attractions = self.attraction_data.get('attractions', [])
            
            recommended = []
            for attraction in attractions:
                score = 0
                
                # Score based on trip type
                if preferences.trip_type.value in attraction.get('tags', []):
                    score += 3
                
                # Score based on interests
                for interest in preferences.interests:
                    if interest.lower() in attraction.get('description', '').lower():
                        score += 2
                
                # Score based on budget
                if attraction.get('cost', 0) <= self._get_budget_threshold(preferences.budget_level):
                    score += 1
                
                if score > 0:
                    recommended.append({
                        'name': attraction['name'],
                        'description': attraction['description'],
                        'location': attraction['location'],
                        'cost': attraction.get('cost', 0),
                        'score': score,
                        'best_time': attraction.get('best_time', ''),
                        'tips': attraction.get('tips', [])
                    })
            
            # Sort by score and return top recommendations
            recommended.sort(key=lambda x: x['score'], reverse=True)
            return recommended[:10]
            
        except Exception as e:
            logger.error(f"Error getting attraction recommendations: {str(e)}")
            return []
    
    def _get_budget_threshold(self, budget_level: BudgetLevel) -> float:
        """Get budget threshold for recommendations."""
        thresholds = {
            BudgetLevel.BUDGET: 50,
            BudgetLevel.MODERATE: 150,
            BudgetLevel.LUXURY: 500
        }
        return thresholds.get(budget_level, 150)
    
    def _get_accommodation_recommendations(self, preferences: TripPreferences) -> List[Dict]:
        """Get accommodation recommendations."""
        try:
            accommodations = self.accommodation_data.get('accommodations', [])
            
            recommended = []
            for acc in accommodations:
                if (acc.get('type') == preferences.accommodation_type and
                    acc.get('budget_level') == preferences.budget_level.value):
                    recommended.append({
                        'name': acc['name'],
                        'type': acc['type'],
                        'location': acc['location'],
                        'price_range': acc['price_range'],
                        'amenities': acc.get('amenities', []),
                        'rating': acc.get('rating', 0),
                        'description': acc.get('description', '')
                    })
            
            return recommended[:5]
            
        except Exception as e:
            logger.error(f"Error getting accommodation recommendations: {str(e)}")
            return []
    
    def _get_restaurant_recommendations(self, preferences: TripPreferences) -> List[Dict]:
        """Get restaurant recommendations."""
        try:
            restaurants = self.activity_data.get('restaurants', [])
            
            recommended = []
            for restaurant in restaurants:
                # Check dietary restrictions
                if self._meets_dietary_requirements(restaurant, preferences.dietary_restrictions):
                    recommended.append({
                        'name': restaurant['name'],
                        'cuisine': restaurant['cuisine'],
                        'location': restaurant['location'],
                        'price_range': restaurant['price_range'],
                        'specialties': restaurant.get('specialties', []),
                        'dietary_options': restaurant.get('dietary_options', [])
                    })
            
            return recommended[:8]
            
        except Exception as e:
            logger.error(f"Error getting restaurant recommendations: {str(e)}")
            return []
    
    def _meets_dietary_requirements(self, restaurant: Dict, restrictions: List[str]) -> bool:
        """Check if restaurant meets dietary requirements."""
        try:
            if not restrictions:
                return True
            
            restaurant_options = restaurant.get('dietary_options', [])
            for restriction in restrictions:
                if restriction.lower() not in [opt.lower() for opt in restaurant_options]:
                    return False
            return True
            
        except Exception:
            return True
    
    def _get_activity_recommendations(self, preferences: TripPreferences) -> List[Dict]:
        """Get activity recommendations."""
        try:
            activities = self.activity_data.get('activities', [])
            
            recommended = []
            for activity in activities:
                score = 0
                
                # Score based on trip type
                if preferences.trip_type.value in activity.get('tags', []):
                    score += 2
                
                # Score based on interests
                for interest in preferences.interests:
                    if interest.lower() in activity.get('description', '').lower():
                        score += 1
                
                if score > 0:
                    recommended.append({
                        'name': activity['name'],
                        'description': activity['description'],
                        'duration': activity['duration'],
                        'cost': activity.get('cost', 0),
                        'location': activity['location'],
                        'score': score,
                        'best_time': activity.get('best_time', ''),
                        'requirements': activity.get('requirements', [])
                    })
            
            recommended.sort(key=lambda x: x['score'], reverse=True)
            return recommended[:10]
            
        except Exception as e:
            logger.error(f"Error getting activity recommendations: {str(e)}")
            return []
    
    def _get_transport_recommendations(self, preferences: TripPreferences) -> List[Dict]:
        """Get transport recommendations."""
        try:
            transport_options = self.transport_data.get('options', [])
            
            recommended = []
            for option in transport_options:
                if option.get('budget_level') == preferences.budget_level.value:
                    recommended.append({
                        'type': option['type'],
                        'description': option['description'],
                        'cost_range': option['cost_range'],
                        'pros': option.get('pros', []),
                        'cons': option.get('cons', []),
                        'best_for': option.get('best_for', ''),
                        'booking_tips': option.get('booking_tips', [])
                    })
            
            return recommended
            
        except Exception as e:
            logger.error(f"Error getting transport recommendations: {str(e)}")
            return []
    
    def _get_travel_tips(self, preferences: TripPreferences) -> List[str]:
        """Get personalized travel tips."""
        try:
            tips = []
            
            # Season-specific tips
            if preferences.preferred_season == Season.PEAK:
                tips.extend([
                    'Book accommodations 3-6 months in advance',
                    'Expect higher prices and larger crowds',
                    'Make restaurant reservations early',
                    'Plan outdoor activities for early morning or late afternoon'
                ])
            elif preferences.preferred_season == Season.LOW:
                tips.extend([
                    'Great deals on accommodations and activities',
                    'Pack rain gear and waterproof clothing',
                    'Indoor activities recommended during monsoon',
                    'Fewer crowds but some attractions may have limited hours'
                ])
            
            # Budget-specific tips
            if preferences.budget_level == BudgetLevel.BUDGET:
                tips.extend([
                    'Use public transportation when possible',
                    'Eat at local restaurants and street food stalls',
                    'Stay in guesthouses or hostels',
                    'Look for free activities and attractions'
                ])
            elif preferences.budget_level == BudgetLevel.LUXURY:
                tips.extend([
                    'Consider private guides for personalized experiences',
                    'Book luxury accommodations with spa services',
                    'Private transportation for comfort and convenience',
                    'Fine dining experiences at top restaurants'
                ])
            
            # Group size tips
            if preferences.group_size > 4:
                tips.extend([
                    'Book group accommodations early',
                    'Consider private transportation for convenience',
                    'Plan activities that accommodate larger groups',
                    'Make group reservations for restaurants'
                ])
            
            return tips
            
        except Exception as e:
            logger.error(f"Error getting travel tips: {str(e)}")
            return []
    
    def get_user_trips(self, user_id: str) -> List[Dict]:
        """Get all trips for a user."""
        try:
            if user_id in self.user_trips:
                return [asdict(trip) for trip in self.user_trips[user_id]]
            return []
        except Exception as e:
            logger.error(f"Error getting user trips: {str(e)}")
            return []
    
    def get_trip_details(self, trip_id: str) -> Optional[Dict]:
        """Get detailed information about a specific trip."""
        try:
            for user_trips in self.user_trips.values():
                for trip in user_trips:
                    if trip.trip_id == trip_id:
                        return asdict(trip)
            return None
        except Exception as e:
            logger.error(f"Error getting trip details: {str(e)}")
            return None
    
    def update_trip(self, trip_id: str, updates: Dict) -> bool:
        """Update trip details."""
        try:
            for user_trips in self.user_trips.values():
                for trip in user_trips:
                    if trip.trip_id == trip_id:
                        # Update trip fields
                        for key, value in updates.items():
                            if hasattr(trip, key):
                                setattr(trip, key, value)
                        
                        trip.updated_at = datetime.now()
                        return True
            return False
        except Exception as e:
            logger.error(f"Error updating trip: {str(e)}")
            return False
    
    def delete_trip(self, trip_id: str) -> bool:
        """Delete a trip."""
        try:
            for user_id, user_trips in self.user_trips.items():
                for i, trip in enumerate(user_trips):
                    if trip.trip_id == trip_id:
                        del user_trips[i]
                        return True
            return False
        except Exception as e:
            logger.error(f"Error deleting trip: {str(e)}")
            return False
    
    def _initialize_trip_templates(self) -> Dict:
        """Initialize trip templates for different types."""
        return {
            'cultural': {
                'name': 'Cultural Heritage Tour',
                'description': 'Explore Sri Lanka\'s rich cultural heritage',
                'daily_plans': [
                    {
                        'day_number': 1,
                        'location': 'Colombo',
                        'activities': [
                            {
                                'name': 'Arrival & Welcome',
                                'description': 'Arrive in Colombo and check into hotel',
                                'duration': '2 hours',
                                'cost': 0,
                                'type': 'arrival'
                            },
                            {
                                'name': 'Colombo City Tour',
                                'description': 'Explore Colombo\'s cultural sites',
                                'duration': '4 hours',
                                'cost': 40,
                                'type': 'sightseeing'
                            }
                        ],
                        'meals': [
                            {'type': 'dinner', 'suggestion': 'Welcome dinner at local restaurant', 'cost': 30}
                        ],
                        'accommodation': {'type': 'hotel', 'description': 'City center hotel'},
                        'transport': {'type': 'airport_transfer', 'description': 'Airport to hotel', 'cost': 25}
                    },
                    {
                        'day_number': 2,
                        'location': 'Kandy',
                        'activities': [
                            {
                                'name': 'Travel to Kandy',
                                'description': 'Scenic train journey to Kandy',
                                'duration': '3 hours',
                                'cost': 15,
                                'type': 'travel'
                            },
                            {
                                'name': 'Temple of the Sacred Tooth',
                                'description': 'Visit the most sacred Buddhist temple',
                                'duration': '2 hours',
                                'cost': 20,
                                'type': 'cultural'
                            }
                        ],
                        'meals': [
                            {'type': 'lunch', 'suggestion': 'Local restaurant in Kandy', 'cost': 20},
                            {'type': 'dinner', 'suggestion': 'Hotel dinner', 'cost': 25}
                        ],
                        'accommodation': {'type': 'hotel', 'description': 'Kandy hotel'},
                        'transport': {'type': 'train', 'description': 'Colombo to Kandy', 'cost': 15}
                    }
                ]
            },
            'adventure': {
                'name': 'Adventure & Nature Tour',
                'description': 'Thrilling adventures in Sri Lanka\'s natural landscapes',
                'daily_plans': [
                    {
                        'day_number': 1,
                        'location': 'Sigiriya',
                        'activities': [
                            {
                                'name': 'Sigiriya Rock Climb',
                                'description': 'Climb the ancient rock fortress',
                                'duration': '3 hours',
                                'cost': 30,
                                'type': 'adventure'
                            }
                        ],
                        'meals': [
                            {'type': 'lunch', 'suggestion': 'Local restaurant', 'cost': 20}
                        ],
                        'accommodation': {'type': 'guesthouse', 'description': 'Local guesthouse'},
                        'transport': {'type': 'private_vehicle', 'description': 'Airport to Sigiriya', 'cost': 60}
                    }
                ]
            }
        }
    
    def _initialize_attraction_data(self) -> Dict:
        """Initialize attraction data."""
        return {
            'attractions': [
                {
                    'name': 'Sigiriya',
                    'description': 'Ancient palace and fortress complex',
                    'location': 'Central Province',
                    'cost': 30,
                    'tags': ['cultural', 'historical', 'adventure'],
                    'best_time': 'Early morning',
                    'tips': ['Wear comfortable shoes', 'Bring water', 'Visit early to avoid crowds']
                },
                {
                    'name': 'Temple of the Sacred Tooth',
                    'description': 'Most sacred Buddhist temple in Sri Lanka',
                    'location': 'Kandy',
                    'cost': 20,
                    'tags': ['cultural', 'religious', 'historical'],
                    'best_time': 'Morning or evening',
                    'tips': ['Dress modestly', 'Remove shoes before entering', 'Respect local customs']
                }
            ]
        }
    
    def _initialize_accommodation_data(self) -> Dict:
        """Initialize accommodation data."""
        return {
            'accommodations': [
                {
                    'name': 'Luxury Hotel Colombo',
                    'type': 'hotel',
                    'location': 'Colombo',
                    'price_range': '$150-300/night',
                    'budget_level': 'luxury',
                    'amenities': ['WiFi', 'Pool', 'Spa', 'Restaurant'],
                    'rating': 4.8,
                    'description': '5-star luxury hotel in city center'
                },
                {
                    'name': 'Budget Guesthouse',
                    'type': 'guesthouse',
                    'location': 'Kandy',
                    'price_range': '$20-40/night',
                    'budget_level': 'budget',
                    'amenities': ['WiFi', 'Basic amenities'],
                    'rating': 4.2,
                    'description': 'Clean and comfortable budget accommodation'
                }
            ]
        }
    
    def _initialize_transport_data(self) -> Dict:
        """Initialize transport data."""
        return {
            'options': [
                {
                    'type': 'Public Transport',
                    'description': 'Buses and trains',
                    'cost_range': '$5-20/day',
                    'budget_level': 'budget',
                    'pros': ['Cheap', 'Authentic experience', 'Eco-friendly'],
                    'cons': ['Can be crowded', 'Less reliable timing', 'Limited routes'],
                    'best_for': 'Budget travelers, solo travelers',
                    'booking_tips': ['Buy tickets at stations', 'Check schedules in advance', 'Allow extra time']
                },
                {
                    'type': 'Private Vehicle',
                    'description': 'Car with driver',
                    'cost_range': '$80-150/day',
                    'budget_level': 'luxury',
                    'pros': ['Convenient', 'Flexible', 'Comfortable'],
                    'cons': ['Expensive', 'Less authentic', 'Environmental impact'],
                    'best_for': 'Families, groups, luxury travelers',
                    'booking_tips': ['Book in advance', 'Negotiate rates', 'Check driver credentials']
                }
            ]
        }
    
    def _initialize_activity_data(self) -> Dict:
        """Initialize activity data."""
        return {
            'activities': [
                {
                    'name': 'Cultural Dance Show',
                    'description': 'Traditional Sri Lankan dance performance',
                    'duration': '2 hours',
                    'cost': 25,
                    'location': 'Kandy',
                    'tags': ['cultural', 'entertainment'],
                    'best_time': 'Evening',
                    'requirements': ['Booking required', 'Smart casual dress']
                },
                {
                    'name': 'Tea Plantation Tour',
                    'description': 'Visit tea estates and learn about tea production',
                    'duration': '3 hours',
                    'cost': 35,
                    'location': 'Nuwara Eliya',
                    'tags': ['cultural', 'nature', 'educational'],
                    'best_time': 'Morning',
                    'requirements': ['Comfortable walking shoes', 'Weather appropriate clothing']
                }
            ],
            'restaurants': [
                {
                    'name': 'Traditional Sri Lankan Restaurant',
                    'cuisine': 'Sri Lankan',
                    'location': 'Colombo',
                    'price_range': '$15-30/person',
                    'specialties': ['Rice and Curry', 'Hoppers', 'Kottu Roti'],
                    'dietary_options': ['Vegetarian', 'Vegan', 'Gluten-free']
                },
                {
                    'name': 'Seafood Restaurant',
                    'cuisine': 'Seafood',
                    'location': 'Galle',
                    'price_range': '$25-50/person',
                    'specialties': ['Fresh Fish', 'Prawn Curry', 'Crab Dishes'],
                    'dietary_options': ['Seafood', 'Vegetarian']
                }
            ]
        }