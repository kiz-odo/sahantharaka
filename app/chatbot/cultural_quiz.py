"""
Cultural Quiz Component

Provides interactive quizzes and games about Sri Lankan culture,
history, and traditions to engage tourists and promote learning.
"""

import logging
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class CulturalQuizHandler:
    """
    Handles cultural quizzes and games for Sri Lankan tourism education.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the cultural quiz handler.
        
        Args:
            config: Configuration dictionary for quiz settings
        """
        self.config = config or {}
        self.quiz_categories = ['history', 'culture', 'food', 'geography', 'traditions']
        self.quizzes = self._initialize_quizzes()
        self.user_progress = {}
        
        logger.info("Cultural Quiz Handler initialized successfully")
    
    def _initialize_quizzes(self) -> Dict:
        """Initialize quiz questions and answers."""
        return {
            'history': [
                {
                    'id': 'hist_001',
                    'question': 'What ancient city was the capital of Sri Lanka from 377 BC to 1017 AD?',
                    'question_si': 'ක්‍රි.පූ. 377 සිට ක්‍රි.ව. 1017 දක්වා ශ්‍රී ලංකාවේ අගනුවර වූ පුරාණ නගරය කුමක්ද?',
                    'question_ta': 'கி.மு. 377 முதல் கி.பி. 1017 வரை இலங்கையின் தலைநகராக இருந்த பழைய நகரம் எது?',
                    'options': ['Anuradhapura', 'Polonnaruwa', 'Kandy', 'Colombo'],
                    'options_si': ['අනුරාධපුර', 'පොළොන්නරුව', 'මහනුවර', 'කොළඹ'],
                    'options_ta': ['அனுராதபுரம்', 'பொலன்னறுவை', 'கண்டி', 'கொழும்பு'],
                    'correct_answer': 0,
                    'explanation': 'Anuradhapura was the first capital of Sri Lanka and remained so for over 1400 years.',
                    'explanation_si': 'අනුරාධපුර ශ්‍රී ලංකාවේ පළමු අගනුවර වූ අතර එය වසර 1400 කට වැඩි කාලයක් පවතී.',
                    'explanation_ta': 'அனுராதபுரம் இலங்கையின் முதல் தலைநகராக இருந்தது மற்றும் 1400 ஆண்டுகளுக்கும் மேலாக இருந்தது.',
                    'difficulty': 'easy',
                    'points': 10
                },
                {
                    'id': 'hist_002',
                    'question': 'Who built the famous Sigiriya rock fortress?',
                    'question_si': 'ප්‍රසිද්ධ සීගිරිය ගල් බලකොටුව තැනූයේ කවුද?',
                    'question_ta': 'பிரபலமான சிகிரியா பாறை கோட்டையை யார் கட்டினார்?',
                    'options': ['King Dutugemunu', 'King Kasyapa', 'King Parakramabahu', 'King Vijayabahu'],
                    'options_si': ['රජ දුටුගැමුණු', 'රජ කාශ්‍යප', 'රජ පරාක්‍රමබාහු', 'රජ විජයබාහු'],
                    'options_ta': ['அரசர் துட்டுகேமுனு', 'அரசர் காசியப்பா', 'அரசர் பராக்ரமபாகு', 'அரசர் விஜயபாகு'],
                    'correct_answer': 1,
                    'explanation': 'King Kasyapa built Sigiriya in the 5th century AD as his palace and fortress.',
                    'explanation_si': 'රජ කාශ්‍යප ක්‍රි.ව. 5 වන සියවසේ සීගිරිය ඔහුගේ මාලිගාව සහ බලකොටුව ලෙස තැනීය.',
                    'explanation_ta': 'அரசர் காசியப்பா கி.பி. 5 ஆம் நூற்றாண்டில் சிகிரியாவை தனது அரண்மனை மற்றும் கோட்டையாக கட்டினார்.',
                    'difficulty': 'medium',
                    'points': 15
                }
            ],
            'culture': [
                {
                    'id': 'cult_001',
                    'question': 'What is the traditional dance form of Sri Lanka?',
                    'question_si': 'ශ්‍රී ලංකාවේ සම්ප්‍රදායික නැටුම් ආකාරය කුමක්ද?',
                    'question_ta': 'இலங்கையின் பாரம்பரிய நடன வடிவம் என்ன?',
                    'options': ['Bharatanatyam', 'Kathak', 'Kandyan Dance', 'Odissi'],
                    'options_si': ['භරත නාට්‍යම්', 'කතක්', 'උඩරට නැටුම්', 'ඔඩිසි'],
                    'options_ta': ['பரதநாட்டியம்', 'கதக்', 'கண்டி நடனம்', 'ஒடிசி'],
                    'correct_answer': 2,
                    'explanation': 'Kandyan Dance is the traditional dance form originating from the Kandy region.',
                    'explanation_si': 'උඩරට නැටුම් කන්ද උපතිකාවෙන් ආරම්භ වූ සම්ප්‍රදායික නැටුම් ආකාරයයි.',
                    'explanation_ta': 'கண்டி நடனம் கண்டி பிராந்தியத்தில் தோன்றிய பாரம்பரிய நடன வடிவமாகும்.',
                    'difficulty': 'easy',
                    'points': 10
                }
            ],
            'food': [
                {
                    'id': 'food_001',
                    'question': 'What is the national dish of Sri Lanka?',
                    'question_si': 'ශ්‍රී ලංකාවේ ජාතික ආහාරය කුමක්ද?',
                    'question_ta': 'இலங்கையின் தேசிய உணவு என்ன?',
                    'options': ['Rice and Curry', 'Hoppers', 'Kottu Roti', 'Lamprais'],
                    'options_si': ['බත් සහ කරවල', 'ආප්ප', 'කොට්ටු රෝටි', 'ලම්ප්‍රයිස්'],
                    'options_ta': ['அரிசி மற்றும் கறி', 'அப்பம்', 'கொட்டு ரோட்டி', 'லம்பிரைஸ்'],
                    'correct_answer': 0,
                    'explanation': 'Rice and Curry is considered the national dish, consisting of rice with various curries.',
                    'explanation_si': 'බත් සහ කරවල ජාතික ආහාරය ලෙස සලකනු ලබන අතර, එය විවිධ කරවල සමඟ බත් වලින් සමන්විත වේ.',
                    'explanation_ta': 'அரிசி மற்றும் கறி தேசிய உணவாக கருதப்படுகிறது, இது பல்வேறு கறிகளுடன் அரிசியைக் கொண்டுள்ளது.',
                    'difficulty': 'easy',
                    'points': 10
                }
            ]
        }
    
    def get_quiz_categories(self, language: str = 'en') -> List[Dict]:
        """Get available quiz categories."""
        categories = []
        for category in self.quiz_categories:
            category_info = {
                'id': category,
                'name': self._get_category_name(category, language),
                'description': self._get_category_description(category, language),
                'question_count': len(self.quizzes.get(category, [])),
                'difficulty_levels': self._get_difficulty_levels(category)
            }
            categories.append(category_info)
        return categories
    
    def get_quiz_questions(self, category: str, difficulty: str = 'all', 
                          language: str = 'en', count: int = 5) -> List[Dict]:
        """Get quiz questions for a specific category and difficulty."""
        if category not in self.quizzes:
            return []
        
        questions = self.quizzes[category]
        
        # Filter by difficulty if specified
        if difficulty != 'all':
            questions = [q for q in questions if q['difficulty'] == difficulty]
        
        # Randomize and limit count
        random.shuffle(questions)
        questions = questions[:count]
        
        # Format questions for the specified language
        formatted_questions = []
        for question in questions:
            formatted_q = {
                'id': question['id'],
                'question': question[f'question_{language}'] if f'question_{language}' in question else question['question'],
                'options': question[f'options_{language}'] if f'options_{language}' in question else question['options'],
                'difficulty': question['difficulty'],
                'points': question['points']
            }
            formatted_questions.append(formatted_q)
        
        return formatted_questions
    
    def submit_quiz_answer(self, user_id: str, question_id: str, 
                          selected_answer: int, language: str = 'en') -> Dict:
        """Submit and grade a quiz answer."""
        try:
            # Find the question
            question = self._find_question_by_id(question_id)
            if not question:
                return {
                    'success': False,
                    'error': 'Question not found'
                }
            
            # Check if answer is correct
            is_correct = selected_answer == question['correct_answer']
            points_earned = question['points'] if is_correct else 0
            
            # Update user progress
            self._update_user_progress(user_id, question_id, is_correct, points_earned)
            
            # Prepare response
            response = {
                'success': True,
                'is_correct': is_correct,
                'points_earned': points_earned,
                'correct_answer': question['correct_answer'],
                'explanation': question[f'explanation_{language}'] if f'explanation_{language}' in question else question['explanation'],
                'total_points': self._get_user_total_points(user_id),
                'questions_answered': self._get_user_questions_answered(user_id)
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error submitting quiz answer: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user_progress(self, user_id: str, language: str = 'en') -> Dict:
        """Get user's quiz progress and achievements."""
        if user_id not in self.user_progress:
            return {
                'total_points': 0,
                'questions_answered': 0,
                'correct_answers': 0,
                'accuracy': 0.0,
                'categories_completed': [],
                'achievements': []
            }
        
        progress = self.user_progress[user_id]
        total_questions = progress.get('questions_answered', 0)
        correct_answers = progress.get('correct_answers', 0)
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        return {
            'total_points': progress.get('total_points', 0),
            'questions_answered': total_questions,
            'correct_answers': correct_answers,
            'accuracy': round(accuracy, 1),
            'categories_completed': self._get_completed_categories(user_id),
            'achievements': self._get_user_achievements(user_id, language)
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get quiz leaderboard."""
        leaderboard = []
        
        for user_id, progress in self.user_progress.items():
            leaderboard.append({
                'user_id': user_id,
                'total_points': progress.get('total_points', 0),
                'questions_answered': progress.get('questions_answered', 0),
                'accuracy': progress.get('accuracy', 0.0)
            })
        
        # Sort by total points (descending)
        leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
        
        return leaderboard[:limit]
    
    def _get_category_name(self, category: str, language: str) -> str:
        """Get category name in specified language."""
        names = {
            'history': {'en': 'History', 'si': 'ඉතිහාසය', 'ta': 'வரலாறு'},
            'culture': {'en': 'Culture', 'si': 'සංස්කෘතිය', 'ta': 'பண்பாடு'},
            'food': {'en': 'Food & Cuisine', 'si': 'ආහාර සහ උපකරණ', 'ta': 'உணவு மற்றும் சமையல்'},
            'geography': {'en': 'Geography', 'si': 'භූගෝල විද්‍යාව', 'ta': 'புவியியல்'},
            'traditions': {'en': 'Traditions', 'si': 'සම්ප්‍රදායන්', 'ta': 'பாரம்பரியங்கள்'}
        }
        return names.get(category, {}).get(language, category.title())
    
    def _get_category_description(self, category: str, language: str) -> str:
        """Get category description in specified language."""
        descriptions = {
            'history': {
                'en': 'Learn about Sri Lanka\'s rich historical heritage',
                'si': 'ශ්‍රී ලංකාවේ සමෘද්ධ ඓතිහාසික උරුමය ගැන දැනගන්න',
                'ta': 'இலங்கையின் செழுமையான வரலாற்று பாரம்பரியத்தைப் பற்றி அறியுங்கள்'
            },
            'culture': {
                'en': 'Explore the diverse cultural traditions of Sri Lanka',
                'si': 'ශ්‍රී ලංකාවේ විවිධ සංස්කෘතික සම්ප්‍රදායන් ගවේෂණය කරන්න',
                'ta': 'இலங்கையின் பல்வேறு கலாச்சார பாரம்பரியங்களை ஆராயுங்கள்'
            }
        }
        return descriptions.get(category, {}).get(language, 'Test your knowledge')
    
    def _get_difficulty_levels(self, category: str) -> List[str]:
        """Get available difficulty levels for a category."""
        if category not in self.quizzes:
            return []
        
        difficulties = set(q['difficulty'] for q in self.quizzes[category])
        return sorted(list(difficulties))
    
    def _find_question_by_id(self, question_id: str) -> Optional[Dict]:
        """Find a question by its ID."""
        for category_questions in self.quizzes.values():
            for question in category_questions:
                if question['id'] == question_id:
                    return question
        return None
    
    def _update_user_progress(self, user_id: str, question_id: str, 
                             is_correct: bool, points_earned: int):
        """Update user progress after answering a question."""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {
                'total_points': 0,
                'questions_answered': 0,
                'correct_answers': 0,
                'questions': {}
            }
        
        progress = self.user_progress[user_id]
        progress['total_points'] += points_earned
        progress['questions_answered'] += 1
        
        if is_correct:
            progress['correct_answers'] += 1
        
        # Store question result
        progress['questions'][question_id] = {
            'answered_at': datetime.now().isoformat(),
            'is_correct': is_correct,
            'points_earned': points_earned
        }
    
    def _get_user_total_points(self, user_id: str) -> int:
        """Get user's total points."""
        if user_id not in self.user_progress:
            return 0
        return self.user_progress[user_id].get('total_points', 0)
    
    def _get_user_questions_answered(self, user_id: str) -> int:
        """Get number of questions answered by user."""
        if user_id not in self.user_progress:
            return 0
        return self.user_progress[user_id].get('questions_answered', 0)
    
    def _get_completed_categories(self, user_id: str) -> List[str]:
        """Get categories where user has answered all questions."""
        if user_id not in self.user_progress:
            return []
        
        completed = []
        user_questions = set(self.user_progress[user_id]['questions'].keys())
        
        for category, questions in self.quizzes.items():
            category_question_ids = {q['id'] for q in questions}
            if category_question_ids.issubset(user_questions):
                completed.append(category)
        
        return completed
    
    def _get_user_achievements(self, user_id: str, language: str) -> List[Dict]:
        """Get user's achievements based on their progress."""
        if user_id not in self.user_progress:
            return []
        
        progress = self.user_progress[user_id]
        achievements = []
        
        # Points-based achievements
        total_points = progress.get('total_points', 0)
        if total_points >= 100:
            achievements.append({
                'id': 'points_100',
                'name': self._get_achievement_name('points_100', language),
                'description': self._get_achievement_description('points_100', language),
                'unlocked_at': datetime.now().isoformat()
            })
        
        # Accuracy-based achievements
        accuracy = progress.get('correct_answers', 0) / max(progress.get('questions_answered', 1), 1) * 100
        if accuracy >= 80:
            achievements.append({
                'id': 'accuracy_80',
                'name': self._get_achievement_name('accuracy_80', language),
                'description': self._get_achievement_description('accuracy_80', language),
                'unlocked_at': datetime.now().isoformat()
            })
        
        return achievements
    
    def _get_achievement_name(self, achievement_id: str, language: str) -> str:
        """Get achievement name in specified language."""
        names = {
            'points_100': {
                'en': 'Quiz Master',
                'si': 'විභාග මාස්ටර්',
                'ta': 'வினாடி வினா மாஸ்டர்'
            },
            'accuracy_80': {
                'en': 'Sharp Mind',
                'si': 'තියුණු මනස',
                'ta': 'கூர்மையான மனம்'
            }
        }
        return names.get(achievement_id, {}).get(language, 'Achievement')
    
    def _get_achievement_description(self, achievement_id: str, language: str) -> str:
        """Get achievement description in specified language."""
        descriptions = {
            'points_100': {
                'en': 'Earned 100 points by answering quiz questions correctly',
                'si': 'විභාග ප්‍රශ්නවලට නිවැරදිව පිළිතුරු දීමෙන් ලකුණු 100 ක් ලබා ගත්තා',
                'ta': 'வினாடி வினாக்களுக்கு சரியாக பதிலளிப்பதன் மூலம் 100 புள்ளிகள் பெற்றார்'
            },
            'accuracy_80': {
                'en': 'Maintained 80% accuracy in quiz answers',
                'si': 'විභාග පිළිතුරු වල 80% නිරවද්‍යතාවය පවත්වා ගත්තා',
                'ta': 'வினாடி வினா பதில்களில் 80% துல்லியத்தை பராமரித்தார்'
            }
        }
        return descriptions.get(achievement_id, {}).get(language, 'Achievement unlocked')
    
    def get_quiz_stats(self) -> Dict:
        """Get overall quiz statistics."""
        total_questions = sum(len(questions) for questions in self.quizzes.values())
        total_users = len(self.user_progress)
        
        return {
            'total_categories': len(self.quiz_categories),
            'total_questions': total_questions,
            'total_users': total_users,
            'categories': {
                category: {
                    'question_count': len(questions),
                    'difficulty_distribution': self._get_difficulty_distribution(questions)
                }
                for category, questions in self.quizzes.items()
            }
        }
    
    def _get_difficulty_distribution(self, questions: List[Dict]) -> Dict:
        """Get distribution of questions by difficulty level."""
        distribution = {}
        for question in questions:
            difficulty = question['difficulty']
            distribution[difficulty] = distribution.get(difficulty, 0) + 1
        return distribution