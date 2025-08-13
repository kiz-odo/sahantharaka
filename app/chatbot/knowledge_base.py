"""
Tourism Knowledge Base for Sri Lanka Tourism Chatbot

Contains comprehensive information about Sri Lankan tourism in multiple languages
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TourismKnowledgeBase:
    """
    Comprehensive tourism knowledge base for Sri Lanka
    Supports 5 languages: English, Sinhala, Tamil, Chinese, and French
    """
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.cultural_context = self._initialize_cultural_context()
        self.emergency_info = self._initialize_emergency_info()
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize the main tourism knowledge base"""
        return {
            'attractions': {
                'en': {
                    'sigiriya': {
                        'name': 'Sigiriya Rock Fortress',
                        'description': 'Ancient rock fortress and palace ruins with stunning frescoes and panoramic views',
                        'location': 'Central Province, near Dambulla',
                        'type': 'Historical Site',
                        'best_time': 'Early morning or late afternoon',
                        'duration': '3-4 hours',
                        'entry_fee': 'LKR 5,000 for foreigners',
                        'tips': 'Carry water, wear comfortable shoes, start early to avoid crowds'
                    },
                    'kandy': {
                        'name': 'Temple of the Tooth Relic (Sri Dalada Maligawa)',
                        'description': 'Sacred Buddhist temple housing a tooth relic of Buddha',
                        'location': 'Kandy, Central Province',
                        'type': 'Religious Site',
                        'best_time': 'During puja ceremonies (6:30 AM, 12:30 PM, 7:30 PM)',
                        'duration': '2-3 hours',
                        'entry_fee': 'LKR 1,500',
                        'tips': 'Dress modestly, remove shoes before entering, photography restrictions apply'
                    },
                    'galle_fort': {
                        'name': 'Galle Fort',
                        'description': 'Well-preserved colonial fort with Dutch architecture and stunning ocean views',
                        'location': 'Galle, Southern Province',
                        'type': 'Historical Site',
                        'best_time': 'Late afternoon for sunset views',
                        'duration': '2-3 hours',
                        'entry_fee': 'Free to walk around, paid attractions inside',
                        'tips': 'Perfect for sunset photography, many cafes and shops inside'
                    }
                },
                'si': {
                    'sigiriya': {
                        'name': 'සීගිරිය පර්වත කොටුව',
                        'description': 'පුරාණ පර්වත කොටුවක් සහ මාලිගා නටබුන් සුන්දර චිත්‍ර සහ පරිදර්ශන සමග',
                        'location': 'මධ්‍යම පළාත, දඹුල්ල අසල',
                        'type': 'ඓතිහාසික ස්ථානය',
                        'best_time': 'පාන්දර උදේ හෝ සවස් වරුවේ',
                        'duration': 'පැය 3-4',
                        'entry_fee': 'විදේශිකයන්ට රුපියල් 5,000',
                        'tips': 'ජලය රැගෙන යන්න, සුවපහසු සපත්තු ඇඳන්න, සමූහය වළකා ගැනීමට කල්තියා පටන් ගන්න'
                    }
                },
                'ta': {
                    'sigiriya': {
                        'name': 'சீகிரியா பாறை கோட்டை',
                        'description': 'அழகான ஓவியங்கள் மற்றும் பரந்த காட்சிகளுடன் கூடிய பண்டைய பாறை கோட்டை மற்றும் அரண்மனை இடிபாடுகள்',
                        'location': 'மத்திய மாகாணம், தம்புள்ளை அருகே',
                        'type': 'வரலாற்று இடம்',
                        'best_time': 'அதிகாலை அல்லது மாலை',
                        'duration': '3-4 மணி நேரம்',
                        'entry_fee': 'வெளிநாட்டவர்களுக்கு LKR 5,000',
                        'tips': 'தண்ணீர் எடுத்துச் செல்லுங்கள், வசதியான காலணிகள் அணியுங்கள், கூட்டத்தைத் தவிர்க்க சீக்கிரம் தொடங்குங்கள்'
                    }
                },
                'zh': {
                    'sigiriya': {
                        'name': '狮子岩古堡',
                        'description': '拥有精美壁画和全景的古代岩石要塞和宫殿遗址',
                        'location': '中央省，丹布勒附近',
                        'type': '历史遗址',
                        'best_time': '清晨或傍晚',
                        'duration': '3-4小时',
                        'entry_fee': '外国人5000卢比',
                        'tips': '携带水，穿舒适的鞋子，早起避免人群'
                    }
                },
                'fr': {
                    'sigiriya': {
                        'name': 'Forteresse de Sigiriya',
                        'description': 'Ancienne forteresse de roche et ruines de palais avec de superbes fresques et vues panoramiques',
                        'location': 'Province centrale, près de Dambulla',
                        'type': 'Site historique',
                        'best_time': 'Tôt le matin ou en fin d\'après-midi',
                        'duration': '3-4 heures',
                        'entry_fee': '5 000 LKR pour les étrangers',
                        'tips': 'Apportez de l\'eau, portez des chaussures confortables, commencez tôt pour éviter les foules'
                    }
                }
            },
            'food': {
                'en': {
                    'rice_curry': {
                        'name': 'Rice and Curry',
                        'description': 'Traditional Sri Lankan meal with rice and various curries',
                        'type': 'Main Dish',
                        'spice_level': 'Medium to Hot',
                        'ingredients': ['Rice', 'Curry leaves', 'Coconut', 'Spices', 'Vegetables/Meat'],
                        'where_to_try': 'Local restaurants, hotels, home stays'
                    },
                    'hoppers': {
                        'name': 'Hoppers (Appa)',
                        'description': 'Bowl-shaped pancakes made from rice flour and coconut milk',
                        'type': 'Breakfast/Dinner',
                        'spice_level': 'Mild',
                        'varieties': ['Plain hoppers', 'Egg hoppers', 'String hoppers'],
                        'where_to_try': 'Street food stalls, local eateries'
                    }
                },
                'si': {
                    'rice_curry': {
                        'name': 'බත් සහ කරි',
                        'description': 'බත් සහ විවිධ කරි වර්ග සමඟ සාම්ප්‍රදායික ශ්‍රී ලාංකික ආහාරය',
                        'type': 'ප්‍රධාන ආහාරය',
                        'spice_level': 'මධ්‍යම සිට උණුසුම්',
                        'ingredients': ['බත්', 'කරපිංචා', 'පොල්', 'කුළුබඩු', 'එළවලු/මස්'],
                        'where_to_try': 'ප්‍රාදේශීය ආපනශාලා, හෝටල්, ගෘහ නවාතැන්'
                    }
                }
            },
            'transport': {
                'en': {
                    'train': {
                        'description': 'Scenic train journeys through tea plantations and mountains',
                        'popular_routes': [
                            'Colombo to Kandy',
                            'Kandy to Ella (most scenic)',
                            'Colombo to Galle'
                        ],
                        'booking': 'Online via railway.gov.lk or at stations',
                        'classes': ['1st Class A/C', '2nd Class', '3rd Class'],
                        'tips': 'Book in advance, window seats for views'
                    },
                    'bus': {
                        'description': 'Extensive bus network covering the entire island',
                        'types': ['Local buses', 'Inter-city express', 'A/C buses'],
                        'payment': 'Cash only, conductor collects fare',
                        'tips': 'Can be crowded, carry small notes'
                    },
                    'tuk_tuk': {
                        'description': 'Three-wheeler taxis for short distances',
                        'usage': 'City transport, short trips',
                        'payment': 'Negotiate fare beforehand or use meter',
                        'tips': 'Agree on price before starting journey'
                    }
                }
            }
        }
    
    def _initialize_cultural_context(self) -> Dict[str, Any]:
        """Initialize cultural context and etiquette information"""
        return {
            'etiquette': {
                'en': {
                    'greetings': 'Say "Ayubowan" (may you live long) with palms together',
                    'dress_code': 'Dress modestly when visiting temples - cover shoulders and knees',
                    'shoes': 'Remove shoes before entering temples and homes',
                    'head': 'Avoid touching someone\'s head - it\'s considered sacred',
                    'pointing': 'Point with open hand, not index finger',
                    'gifts': 'Use both hands when giving or receiving items'
                },
                'si': {
                    'greetings': 'අත්දෙක එකට තබා "ආයුබෝවන්" කියන්න',
                    'dress_code': 'දේවාල වලට යන විට නිසි ඇඳුමක් ඇඳන්න - උරහිස් සහ දණහිස් ආවරණය කරන්න',
                    'shoes': 'දේවාල සහ නිවස් වලට ඇතුළු වීමට පෙර සපත්තු ගලවන්න',
                    'head': 'කවරෙකුගේ හිස ස්පර්ශ කිරීමෙන් වළකින්න - එය පූජනීය ලෙස සලකනු ලැබේ',
                    'pointing': 'ඇඟිල්ලෙන් නොව විවෘත අතෙන් පෙන්වන්න',
                    'gifts': 'කිසියම් දෙයක් දෙන හෝ ගැනීමේදී අත් දෙකම භාවිතා කරන්න'
                }
            },
            'festivals': {
                'en': {
                    'vesak': {
                        'name': 'Vesak Full Moon Poya Day',
                        'description': 'Celebrates birth, enlightenment, and death of Buddha',
                        'when': 'May (full moon day)',
                        'celebrations': 'Lanterns, free food stalls (dansalas), temple visits',
                        'significance': 'Most important Buddhist festival'
                    },
                    'sinhala_tamil_new_year': {
                        'name': 'Sinhala and Tamil New Year',
                        'description': 'Traditional New Year celebration',
                        'when': 'April 13-14',
                        'celebrations': 'Traditional games, special foods, family gatherings',
                        'significance': 'Cultural New Year for both communities'
                    }
                }
            }
        }
    
    def _initialize_emergency_info(self) -> Dict[str, Any]:
        """Initialize emergency contact information"""
        return {
            'emergency_contacts': {
                'police': '119',
                'fire_ambulance': '110',
                'tourist_police': '1912',
                'tourist_hotline': '+94 11 2421 052'
            },
            'embassies': {
                'us': '+94 11 249 8500',
                'uk': '+94 11 538 9639',
                'australia': '+94 11 246 3200',
                'canada': '+94 11 532 6232'
            }
        }
    
    def get_attraction_info(self, attraction_name: str, language: str = 'en') -> Optional[Dict[str, Any]]:
        """
        Get information about a specific attraction
        
        Args:
            attraction_name (str): Name of the attraction
            language (str): Language code
            
        Returns:
            Optional[Dict[str, Any]]: Attraction information or None if not found
        """
        attractions = self.knowledge_base.get('attractions', {}).get(language, {})
        
        # Search by exact key match first
        if attraction_name.lower() in attractions:
            return attractions[attraction_name.lower()]
        
        # Search by name similarity
        for key, info in attractions.items():
            if attraction_name.lower() in info.get('name', '').lower():
                return info
        
        return None
    
    def get_food_info(self, food_name: str, language: str = 'en') -> Optional[Dict[str, Any]]:
        """
        Get information about Sri Lankan food
        
        Args:
            food_name (str): Name of the food
            language (str): Language code
            
        Returns:
            Optional[Dict[str, Any]]: Food information or None if not found
        """
        foods = self.knowledge_base.get('food', {}).get(language, {})
        
        for key, info in foods.items():
            if food_name.lower() in key or food_name.lower() in info.get('name', '').lower():
                return info
        
        return None
    
    def get_transport_info(self, transport_type: str, language: str = 'en') -> Optional[Dict[str, Any]]:
        """
        Get transportation information
        
        Args:
            transport_type (str): Type of transport
            language (str): Language code
            
        Returns:
            Optional[Dict[str, Any]]: Transport information or None if not found
        """
        transport = self.knowledge_base.get('transport', {}).get(language, {})
        return transport.get(transport_type.lower())
    
    def get_cultural_info(self, topic: str, language: str = 'en') -> Optional[Dict[str, Any]]:
        """
        Get cultural information and etiquette
        
        Args:
            topic (str): Cultural topic
            language (str): Language code
            
        Returns:
            Optional[Dict[str, Any]]: Cultural information or None if not found
        """
        return self.cultural_context.get(topic, {}).get(language)
    
    def get_emergency_info(self, info_type: str = 'all') -> Dict[str, Any]:
        """
        Get emergency contact information
        
        Args:
            info_type (str): Type of emergency info ('all', 'contacts', 'embassies')
            
        Returns:
            Dict[str, Any]: Emergency information
        """
        if info_type == 'contacts':
            return self.emergency_info['emergency_contacts']
        elif info_type == 'embassies':
            return self.emergency_info['embassies']
        else:
            return self.emergency_info
    
    def search_knowledge_base(self, query: str, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant information
        
        Args:
            query (str): Search query
            language (str): Language code
            
        Returns:
            List[Dict[str, Any]]: List of relevant information
        """
        results = []
        query_lower = query.lower()
        
        # Search attractions
        attractions = self.knowledge_base.get('attractions', {}).get(language, {})
        for key, info in attractions.items():
            if (query_lower in key or 
                query_lower in info.get('name', '').lower() or
                query_lower in info.get('description', '').lower()):
                results.append({
                    'type': 'attraction',
                    'key': key,
                    'info': info
                })
        
        # Search food
        foods = self.knowledge_base.get('food', {}).get(language, {})
        for key, info in foods.items():
            if (query_lower in key or 
                query_lower in info.get('name', '').lower() or
                query_lower in info.get('description', '').lower()):
                results.append({
                    'type': 'food',
                    'key': key,
                    'info': info
                })
        
        # Search transport
        transport = self.knowledge_base.get('transport', {}).get(language, {})
        for key, info in transport.items():
            if (query_lower in key or 
                query_lower in info.get('description', '').lower()):
                results.append({
                    'type': 'transport',
                    'key': key,
                    'info': info
                })
        
        return results