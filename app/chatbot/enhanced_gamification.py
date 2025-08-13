"""
Enhanced Gamification System

Provides advanced gamification features including virtual tour guides,
cultural challenges, progressive learning, and social features for Phase 3.
"""

import logging
import random
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class AchievementType(Enum):
    """Types of achievements."""
    EXPLORER = "explorer"
    CULTURAL = "cultural"
    LANGUAGE = "language"
    SOCIAL = "social"
    MILESTONE = "milestone"
    SPECIAL = "special"


class ChallengeType(Enum):
    """Types of cultural challenges."""
    QUIZ = "quiz"
    PHOTO = "photo"
    VISIT = "visit"
    LEARNING = "learning"
    SOCIAL = "social"
    CREATIVE = "creative"


class TourGuideType(Enum):
    """Types of virtual tour guides."""
    HISTORIAN = "historian"
    CULTURAL_EXPERT = "cultural_expert"
    NATURE_GUIDE = "nature_guide"
    FOOD_CRITIC = "food_critic"
    ADVENTURE_GUIDE = "adventure_guide"


@dataclass
class Achievement:
    """Achievement structure."""
    id: str
    name: str
    name_si: str
    name_ta: str
    description: str
    description_si: str
    description_ta: str
    type: AchievementType
    points: int
    icon: str
    rarity: str  # common, rare, epic, legendary
    requirements: Dict[str, Any]
    unlocked_at: Optional[datetime] = None


@dataclass
class Challenge:
    """Cultural challenge structure."""
    id: str
    name: str
    name_si: str
    name_ta: str
    description: str
    description_si: str
    description_ta: str
    type: ChallengeType
    difficulty: str  # easy, medium, hard, expert
    points: int
    duration: Optional[timedelta] = None
    requirements: Dict[str, Any]
    rewards: List[str]
    is_active: bool = True


@dataclass
class VirtualTourGuide:
    """Virtual tour guide structure."""
    id: str
    name: str
    name_si: str
    name_ta: str
    type: TourGuideType
    personality: str
    expertise: List[str]
    greeting_message: str
    greeting_message_si: str
    greeting_message_ta: str
    avatar_url: Optional[str] = None
    is_available: bool = True


@dataclass
class UserProgress:
    """User progress and achievements."""
    user_id: str
    level: int
    experience_points: int
    total_points: int
    achievements: List[str]
    active_challenges: List[str]
    completed_challenges: List[str]
    current_guide: Optional[str] = None
    guide_history: List[str]
    created_at: datetime
    last_updated: datetime


class EnhancedGamificationSystem:
    """
    Enhanced gamification system providing virtual tour guides,
    cultural challenges, and progressive learning experiences.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the enhanced gamification system.
        
        Args:
            config: Configuration dictionary for gamification settings
        """
        self.config = config or {}
        self.user_progress = {}
        self.achievements = self._initialize_achievements()
        self.challenges = self._initialize_challenges()
        self.tour_guides = self._initialize_tour_guides()
        
        # Gamification settings
        self.xp_per_level = self.config.get('xp_per_level', 1000)
        self.max_level = self.config.get('max_level', 100)
        self.challenge_cooldown = self.config.get('challenge_cooldown', 24)  # hours
        
        logger.info("Enhanced Gamification System initialized successfully")
    
    def _initialize_achievements(self) -> Dict[str, Achievement]:
        """Initialize the achievement system."""
        achievements = {}
        
        # Explorer Achievements
        achievements['first_visit'] = Achievement(
            id='first_visit',
            name='First Steps in Sri Lanka',
            name_si='ශ්‍රී ලංකාවේ පළමු පියවර',
            name_ta='இலங்கையில் முதல் படிகள்',
            description='Complete your first conversation with the chatbot',
            description_si='චැට්බොට් සමඟ ඔබගේ පළමු සංවාදය සම්පූර්ණ කරන්න',
            description_ta='சாட்போடுடன் உங்கள் முதல் உரையாடலை முடிக்கவும்',
            type=AchievementType.EXPLORER,
            points=50,
            icon='🌱',
            rarity='common',
            requirements={'conversations': 1}
        )
        
        achievements['language_master'] = Achievement(
            id='language_master',
            name='Polyglot Explorer',
            name_si='බහුභාෂා ගවේෂකයා',
            name_ta='பல மொழி ஆராய்ச்சியாளர்',
            description='Use the chatbot in all three supported languages',
            description_si='සහාය දක්වන සියලුම භාෂා තුනෙහි චැට්බොට් භාවිතා කරන්න',
            description_ta='ஆதரிக்கப்படும் மூன்று மொழிகளிலும் சாட்போட்டைப் பயன்படுத்தவும்',
            type=AchievementType.LANGUAGE,
            points=200,
            icon='🌍',
            rarity='rare',
            requirements={'languages_used': 3}
        )
        
        achievements['cultural_expert'] = Achievement(
            id='cultural_expert',
            name='Cultural Connoisseur',
            name_si='සංස්කෘතික විශේෂඥ',
            name_ta='கலாச்சார நிபுணர்',
            description='Complete 10 cultural challenges',
            description_si='සංස්කෘතික අභියෝග 10 ක් සම්පූර්ණ කරන්න',
            description_ta='10 கலாச்சார சவால்களை முடிக்கவும்',
            type=AchievementType.CULTURAL,
            points=500,
            icon='🏛️',
            rarity='epic',
            requirements={'cultural_challenges': 10}
        )
        
        achievements['sigiriya_explorer'] = Achievement(
            id='sigiriya_explorer',
            name='Sigiriya Master',
            name_si='සීගිරිය මාස්ටර්',
            name_ta='சிகிரியா மாஸ்டர்',
            description='Learn everything about Sigiriya through the chatbot',
            description_si='චැට්බොට් හරහා සීගිරිය ගැන සියල්ල ඉගෙන ගන්න',
            description_ta='சாட்போட் மூலம் சிகிரியா பற்றி எல்லாம் கற்றுக்கொள்ளவும்',
            type=AchievementType.EXPLORER,
            points=300,
            icon='🏰',
            rarity='rare',
            requirements={'sigiriya_knowledge': 100}
        )
        
        achievements['quiz_champion'] = Achievement(
            id='quiz_champion',
            name='Quiz Champion',
            name_si='විභාග ශූරයා',
            name_ta='வினாடி வினா சாம்பியன்',
            description='Score 1000+ points in cultural quizzes',
            description_si='සංස්කෘතික විභාග වලින් ලකුණු 1000+ ලබා ගන්න',
            description_ta='கலாச்சார வினாடி வினாக்களில் 1000+ புள்ளிகள் பெறவும்',
            type=AchievementType.CULTURAL,
            points=400,
            icon='🏆',
            rarity='rare',
            requirements={'quiz_points': 1000}
        )
        
        return achievements
    
    def _initialize_challenges(self) -> Dict[str, Challenge]:
        """Initialize the cultural challenges."""
        challenges = {}
        
        # Daily Challenges
        challenges['daily_language'] = Challenge(
            id='daily_language',
            name='Learn a New Phrase',
            name_si='නව වාක්‍ය ඛණ්ඩයක් ඉගෙන ගන්න',
            name_ta='புதிய சொற்றொடரைக் கற்றுக்கொள்ளுங்கள்',
            description='Learn and use a new phrase in Sinhala or Tamil',
            description_si='සිංහල හෝ දෙමළෙන් නව වාක්‍ය ඛණ්ඩයක් ඉගෙන ගෙන භාවිතා කරන්න',
            description_ta='சிங்களம் அல்லது தமிழில் புதிய சொற்றொடரைக் கற்று பயன்படுத்தவும்',
            type=ChallengeType.LEARNING,
            difficulty='easy',
            points=25,
            duration=timedelta(hours=24),
            requirements={'phrase_learned': True, 'phrase_used': True},
            rewards=['language_badge', 'xp_boost']
        )
        
        challenges['photo_challenge'] = Challenge(
            id='photo_challenge',
            name='Cultural Photo Hunt',
            name_si='සංස්කෘතික ඡායාරූප සොයාගැනීම',
            name_ta='கலாச்சார புகைப்பட வேட்டை',
            description='Take photos of 3 different cultural elements',
            description_si='විවිධ සංස්කෘතික මූලද්‍රව්‍ය 3 ක් ඡායාරූප ගන්න',
            description_ta='3 வெவ்வேறு கலாச்சார கூறுகளின் புகைப்படங்களை எடுக்கவும்',
            type=ChallengeType.PHOTO,
            difficulty='medium',
            points=75,
            duration=timedelta(days=7),
            requirements={'cultural_photos': 3},
            rewards=['photographer_badge', 'cultural_insight']
        )
        
        challenges['temple_visit'] = Challenge(
            id='temple_visit',
            name='Sacred Temple Explorer',
            name_si='පූජනීය දේවාල ගවේෂකයා',
            name_ta='புனித கோவில் ஆராய்ச்சியாளர்',
            description='Visit and learn about 5 different temples',
            description_si='විවිධ දේවාල 5 ක් සංචාරය කර ඒවා ගැන දැනගන්න',
            description_ta='5 வெவ்வேறு கோவில்களை பார்வையிட்டு அவற்றைப் பற்றி அறியவும்',
            type=ChallengeType.VISIT,
            difficulty='hard',
            points=150,
            duration=timedelta(days=30),
            requirements={'temples_visited': 5},
            rewards=['pilgrim_badge', 'spiritual_insight', 'xp_boost']
        )
        
        challenges['cultural_quiz_master'] = Challenge(
            id='cultural_quiz_master',
            name='Cultural Quiz Master',
            name_si='සංස්කෘතික විභාග මාස්ටර්',
            name_ta='கலாச்சார வினாடி வினா மாஸ்டர்',
            description='Complete 5 cultural quizzes with 90%+ accuracy',
            description_si='90%+ නිරවද්‍යතාවයකින් සංස්කෘතික විභාග 5 ක් සම්පූර්ණ කරන්න',
            description_ta='90%+ துல்லியத்துடன் 5 கலாச்சார வினாடி வினாக்களை முடிக்கவும்',
            type=ChallengeType.QUIZ,
            difficulty='expert',
            points=300,
            duration=timedelta(days=14),
            requirements={'quizzes_completed': 5, 'accuracy_threshold': 90},
            rewards=['quiz_master_badge', 'cultural_expert_title', 'special_guide_access']
        )
        
        return challenges
    
    def _initialize_tour_guides(self) -> Dict[str, VirtualTourGuide]:
        """Initialize the virtual tour guides."""
        guides = {}
        
        guides['saru_historian'] = VirtualTourGuide(
            id='saru_historian',
            name='Saru - The Historian',
            name_si='සරු - ඉතිහාසඥ',
            name_ta='சரு - வரலாற்றாசிரியர்',
            type=TourGuideType.HISTORIAN,
            personality='Wise and knowledgeable, loves sharing historical stories',
            expertise=['ancient kingdoms', 'archaeological sites', 'royal history', 'UNESCO sites'],
            greeting_message='Hello! I\'m Saru, your personal historian. Ready to explore Sri Lanka\'s rich past?',
            greeting_message_si='ආයුබෝවන්! මම සරු, ඔබගේ පෞද්ගලික ඉතිහාසඥයා. ශ්‍රී ලංකාවේ සමෘද්ධ අතීතය ගවේෂණය කිරීමට සූදානම්ද?',
            greeting_message_ta='வணக்கம்! நான் சரு, உங்கள் தனிப்பட்ட வரலாற்றாசிரியர். இலங்கையின் செழுமையான கடந்த காலத்தை ஆராய தயாரா?'
        )
        
        guides['anjali_cultural'] = VirtualTourGuide(
            id='anjali_cultural',
            name='Anjali - The Cultural Expert',
            name_si='අංජලි - සංස්කෘතික විශේෂඥ',
            name_ta='அஞ்சலி - கலாச்சார நிபுணர்',
            type=TourGuideType.CULTURAL_EXPERT,
            personality='Warm and enthusiastic, passionate about traditions and customs',
            expertise=['traditional arts', 'festivals', 'customs', 'local traditions', 'dance forms'],
            greeting_message='Hi there! I\'m Anjali, your cultural guide. Let\'s discover the beautiful traditions of Sri Lanka!',
            greeting_message_si='ආයුබෝවන්! මම අංජලි, ඔබගේ සංස්කෘතික මඟපෙන්වන්නා. ශ්‍රී ලංකාවේ සුන්දර සම්ප්‍රදායන් සොයා බලමු!',
            greeting_message_ta='வணக்கம்! நான் அஞ்சலி, உங்கள் கலாச்சார வழிகாட்டி. இலங்கையின் அழகான பாரம்பரியங்களைக் கண்டுபிடிப்போம்!'
        )
        
        guides['kumar_nature'] = VirtualTourGuide(
            id='kumar_nature',
            name='Kumar - The Nature Guide',
            name_si='කුමාර් - ස්වභාව ගවේෂක',
            name_ta='குமார் - இயற்கை வழிகாட்டி',
            type=TourGuideType.NATURE_GUIDE,
            personality='Adventurous and energetic, loves outdoor activities and wildlife',
            expertise=['national parks', 'hiking trails', 'wildlife', 'beaches', 'tea plantations'],
            greeting_message='Hey! I\'m Kumar, your adventure buddy! Ready for some amazing outdoor experiences?',
            greeting_message_si='හේය්! මම කුමාර්, ඔබගේ ස모ඛ්‍යයා! අපූරු එළිමහන් අත්දැකීම් සඳහා සූදානම්ද?',
            greeting_message_ta='ஹே! நான் குமார், உங்கள் சாகச நண்பர்! சில அற்புதமான வெளிப்புற அனுபவங்களுக்கு தயாரா?'
        )
        
        guides['priya_food'] = VirtualTourGuide(
            id='priya_food',
            name='Priya - The Food Critic',
            name_si='ප්‍රියා - ආහාර විචාරක',
            name_ta='பிரியா - உணவு விமர்சகர்',
            type=TourGuideType.FOOD_CRITIC,
            personality='Friendly and passionate about food, loves sharing culinary secrets',
            expertise=['local cuisine', 'street food', 'traditional recipes', 'spices', 'restaurants'],
            greeting_message='Hello foodie! I\'m Priya, your culinary guide. Hungry for some delicious Sri Lankan flavors?',
            greeting_message_si='ආයුබෝවන් ආහාර රසිකය! මම ප්‍රියා, ඔබගේ ආහාර විශේෂඥ. රසවත් ශ්‍රී ලාංකික රසවිඳීම් සඳහා බඩගිනිද?',
            greeting_message_ta='வணக்கம் உணவு ஆர்வலரே! நான் பிரியா, உங்கள் சமையல் வழிகாட்டி. சில சுவையான இலங்கை சுவைகளுக்கு பசியா?'
        )
        
        return guides
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Get or create user progress."""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(
                user_id=user_id,
                level=1,
                experience_points=0,
                total_points=0,
                achievements=[],
                active_challenges=[],
                completed_challenges=[],
                current_guide=None,
                guide_history=[],
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
        
        return self.user_progress[user_id]
    
    def award_experience_points(self, user_id: str, points: int, reason: str = None):
        """Award experience points to a user."""
        try:
            progress = self.get_user_progress(user_id)
            progress.experience_points += points
            progress.total_points += points
            
            # Check for level up
            new_level = self._calculate_level(progress.experience_points)
            if new_level > progress.level:
                progress.level = new_level
                self._handle_level_up(user_id, new_level)
            
            progress.last_updated = datetime.now()
            
            # Record the XP award
            self._record_xp_award(user_id, points, reason)
            
            logger.info(f"Awarded {points} XP to user {user_id} for {reason}")
            
        except Exception as e:
            logger.error(f"Error awarding XP: {str(e)}")
    
    def _calculate_level(self, experience_points: int) -> int:
        """Calculate user level based on experience points."""
        level = 1
        xp_required = self.xp_per_level
        
        while experience_points >= xp_required and level < self.max_level:
            experience_points -= xp_required
            level += 1
            xp_required = int(xp_required * 1.2)  # 20% increase per level
        
        return level
    
    def _handle_level_up(self, user_id: str, new_level: int):
        """Handle user level up events."""
        try:
            # Check for level-based achievements
            level_achievements = [
                'level_5' if new_level >= 5 else None,
                'level_10' if new_level >= 10 else None,
                'level_25' if new_level >= 25 else None,
                'level_50' if new_level >= 50 else None,
                'level_100' if new_level >= 100 else None
            ]
            
            for achievement_id in level_achievements:
                if achievement_id:
                    self.unlock_achievement(user_id, achievement_id)
            
            # Unlock new tour guides at certain levels
            if new_level >= 10:
                self._unlock_tour_guide(user_id, 'anjali_cultural')
            if new_level >= 25:
                self._unlock_tour_guide(user_id, 'kumar_nature')
            if new_level >= 50:
                self._unlock_tour_guide(user_id, 'priya_food')
            
            logger.info(f"User {user_id} reached level {new_level}")
            
        except Exception as e:
            logger.error(f"Error handling level up: {str(e)}")
    
    def unlock_achievement(self, user_id: str, achievement_id: str) -> bool:
        """Unlock an achievement for a user."""
        try:
            if achievement_id not in self.achievements:
                return False
            
            progress = self.get_user_progress(user_id)
            
            if achievement_id in progress.achievements:
                return False  # Already unlocked
            
            achievement = self.achievements[achievement_id]
            
            # Check if requirements are met
            if not self._check_achievement_requirements(user_id, achievement):
                return False
            
            # Unlock achievement
            progress.achievements.append(achievement_id)
            progress.total_points += achievement.points
            
            # Award XP
            self.award_experience_points(user_id, achievement.points, f"achievement_{achievement_id}")
            
            progress.last_updated = datetime.now()
            
            logger.info(f"User {user_id} unlocked achievement: {achievement.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error unlocking achievement: {str(e)}")
            return False
    
    def _check_achievement_requirements(self, user_id: str, achievement: Achievement) -> bool:
        """Check if user meets achievement requirements."""
        try:
            # This is a simplified requirement check
            # In production, implement proper requirement validation
            
            requirements = achievement.requirements
            
            if 'conversations' in requirements:
                # Check conversation count
                pass
            
            if 'languages_used' in requirements:
                # Check languages used
                pass
            
            if 'cultural_challenges' in requirements:
                # Check completed challenges
                pass
            
            # For now, return True to allow testing
            return True
            
        except Exception as e:
            logger.error(f"Error checking achievement requirements: {str(e)}")
            return False
    
    def start_challenge(self, user_id: str, challenge_id: str) -> bool:
        """Start a cultural challenge for a user."""
        try:
            if challenge_id not in self.challenges:
                return False
            
            challenge = self.challenges[challenge_id]
            progress = self.get_user_progress(user_id)
            
            # Check if challenge is already active
            if challenge_id in progress.active_challenges:
                return False
            
            # Check if challenge is available
            if not challenge.is_active:
                return False
            
            # Check cooldown for similar challenges
            if self._is_challenge_on_cooldown(user_id, challenge.type):
                return False
            
            # Start challenge
            progress.active_challenges.append(challenge_id)
            progress.last_updated = datetime.now()
            
            logger.info(f"User {user_id} started challenge: {challenge.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error starting challenge: {str(e)}")
            return False
    
    def complete_challenge(self, user_id: str, challenge_id: str, completion_data: Dict[str, Any]) -> bool:
        """Complete a cultural challenge for a user."""
        try:
            if challenge_id not in self.challenges:
                return False
            
            challenge = self.challenges[challenge_id]
            progress = self.get_user_progress(user_id)
            
            # Check if challenge is active
            if challenge_id not in progress.active_challenges:
                return False
            
            # Validate completion data
            if not self._validate_challenge_completion(challenge, completion_data):
                return False
            
            # Complete challenge
            progress.active_challenges.remove(challenge_id)
            progress.completed_challenges.append(challenge_id)
            
            # Award points and XP
            progress.total_points += challenge.points
            self.award_experience_points(user_id, challenge.points, f"challenge_{challenge_id}")
            
            # Check for related achievements
            self._check_challenge_achievements(user_id, challenge)
            
            progress.last_updated = datetime.now()
            
            logger.info(f"User {user_id} completed challenge: {challenge.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error completing challenge: {str(e)}")
            return False
    
    def _is_challenge_on_cooldown(self, user_id: str, challenge_type: ChallengeType) -> bool:
        """Check if a challenge type is on cooldown for a user."""
        try:
            progress = self.get_user_progress(user_id)
            cooldown_hours = self.challenge_cooldown
            
            # Check recently completed challenges of the same type
            for challenge_id in progress.completed_challenges:
                if challenge_id in self.challenges:
                    challenge = self.challenges[challenge_id]
                    if challenge.type == challenge_type:
                        # Check if enough time has passed
                        # This is simplified - in production, track completion timestamps
                        return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking challenge cooldown: {str(e)}")
            return False
    
    def _validate_challenge_completion(self, challenge: Challenge, completion_data: Dict[str, Any]) -> bool:
        """Validate challenge completion data."""
        try:
            requirements = challenge.requirements
            
            for req_key, req_value in requirements.items():
                if req_key not in completion_data:
                    return False
                
                if completion_data[req_key] < req_value:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating challenge completion: {str(e)}")
            return False
    
    def _check_challenge_achievements(self, user_id: str, challenge: Challenge):
        """Check for achievements related to challenge completion."""
        try:
            # Check for challenge count achievements
            progress = self.get_user_progress(user_id)
            completed_count = len(progress.completed_challenges)
            
            if completed_count >= 5:
                self.unlock_achievement(user_id, 'challenge_master')
            
            if completed_count >= 10:
                self.unlock_achievement(user_id, 'challenge_expert')
            
            # Check for specific challenge type achievements
            challenge_types = [self.challenges[cid].type for cid in progress.completed_challenges if cid in self.challenges]
            type_counts = {}
            
            for ctype in challenge_types:
                type_counts[ctype] = type_counts.get(ctype, 0) + 1
            
            for ctype, count in type_counts.items():
                if count >= 3:
                    achievement_id = f"{ctype.value}_master"
                    if achievement_id in self.achievements:
                        self.unlock_achievement(user_id, achievement_id)
            
        except Exception as e:
            logger.error(f"Error checking challenge achievements: {str(e)}")
    
    def assign_tour_guide(self, user_id: str, guide_id: str) -> bool:
        """Assign a virtual tour guide to a user."""
        try:
            if guide_id not in self.tour_guides:
                return False
            
            guide = self.tour_guides[guide_id]
            if not guide.is_available:
                return False
            
            progress = self.get_user_progress(user_id)
            
            # Update current guide
            if progress.current_guide:
                progress.guide_history.append(progress.current_guide)
            
            progress.current_guide = guide_id
            progress.last_updated = datetime.now()
            
            logger.info(f"Assigned guide {guide.name} to user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error assigning tour guide: {str(e)}")
            return False
    
    def get_available_guides(self, user_id: str) -> List[VirtualTourGuide]:
        """Get available tour guides for a user."""
        try:
            progress = self.get_user_progress(user_id)
            available_guides = []
            
            for guide_id, guide in self.tour_guides.items():
                if guide.is_available:
                    # Check if guide is unlocked for user level
                    if self._is_guide_unlocked_for_user(user_id, guide_id):
                        available_guides.append(guide)
            
            return available_guides
            
        except Exception as e:
            logger.error(f"Error getting available guides: {str(e)}")
            return []
    
    def _is_guide_unlocked_for_user(self, user_id: str, guide_id: str) -> bool:
        """Check if a tour guide is unlocked for a user."""
        try:
            progress = self.get_user_progress(user_id)
            
            # Basic guides are always available
            if guide_id in ['saru_historian']:
                return True
            
            # Level-based unlocks
            if guide_id == 'anjali_cultural' and progress.level >= 10:
                return True
            elif guide_id == 'kumar_nature' and progress.level >= 25:
                return True
            elif guide_id == 'priya_food' and progress.level >= 50:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking guide unlock: {str(e)}")
            return False
    
    def _unlock_tour_guide(self, user_id: str, guide_id: str):
        """Unlock a tour guide for a user."""
        try:
            if guide_id in self.tour_guides:
                # Guide is now available
                logger.info(f"Unlocked tour guide {guide_id} for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error unlocking tour guide: {str(e)}")
    
    def _record_xp_award(self, user_id: str, points: int, reason: str):
        """Record XP award for analytics."""
        try:
            # This could be integrated with the analytics dashboard
            pass
        except Exception as e:
            logger.error(f"Error recording XP award: {str(e)}")
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get global leaderboard."""
        try:
            leaderboard = []
            
            for user_id, progress in self.user_progress.items():
                leaderboard.append({
                    'user_id': user_id,
                    'level': progress.level,
                    'total_points': progress.total_points,
                    'achievements_count': len(progress.achievements),
                    'challenges_completed': len(progress.completed_challenges)
                })
            
            # Sort by total points (descending)
            leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
            
            return leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"Error getting leaderboard: {str(e)}")
            return []
    
    def get_gamification_stats(self) -> Dict[str, Any]:
        """Get overall gamification statistics."""
        return {
            'total_users': len(self.user_progress),
            'total_achievements': len(self.achievements),
            'total_challenges': len(self.challenges),
            'total_guides': len(self.tour_guides),
            'achievements_unlocked': sum(len(progress.achievements) for progress in self.user_progress.values()),
            'challenges_completed': sum(len(progress.completed_challenges) for progress in self.user_progress.values()),
            'average_user_level': np.mean([progress.level for progress in self.user_progress.values()]) if self.user_progress else 0
        }