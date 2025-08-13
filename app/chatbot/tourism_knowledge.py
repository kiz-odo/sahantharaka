"""
Tourism Knowledge Base

Contains comprehensive information about Sri Lanka tourism in multiple languages
including attractions, food, culture, transport, and accommodations.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class TourismKnowledgeBase:
    """
    Comprehensive knowledge base for Sri Lanka tourism information.
    """
    
    def __init__(self):
        """Initialize the tourism knowledge base."""
        self.knowledge = self._initialize_knowledge()
        logger.info("Tourism Knowledge Base initialized successfully")
    
    def _initialize_knowledge(self) -> Dict:
        """Initialize the knowledge base with tourism information."""
        return {
            'attractions': {
                'en': {
                    'sigiriya': {
                        'name': 'Sigiriya',
                        'description': 'Ancient palace and fortress complex built on a massive rock column. Known as the 8th wonder of the world.',
                        'location': 'Central Province, Sri Lanka',
                        'best_time': 'Early morning or late afternoon to avoid crowds and heat',
                        'entrance_fee': 'Approximately $30 USD for foreigners',
                        'highlights': ['Lion\'s Paw entrance', 'Fresco paintings', 'Mirror wall', 'Royal gardens'],
                        'tips': ['Wear comfortable shoes', 'Bring water', 'Visit early morning', 'Hire a guide for history']
                    },
                    'kandy': {
                        'name': 'Kandy',
                        'description': 'Cultural capital of Sri Lanka, home to the Temple of the Sacred Tooth Relic.',
                        'location': 'Central Province, Sri Lanka',
                        'best_time': 'Year-round, but best during Perahera festival (July/August)',
                        'highlights': ['Temple of the Sacred Tooth', 'Royal Botanical Gardens', 'Kandy Lake', 'Cultural shows'],
                        'tips': ['Dress modestly for temple visits', 'Attend cultural dance shows', 'Visit during Perahera']
                    },
                    'galle_fort': {
                        'name': 'Galle Fort',
                        'description': 'UNESCO World Heritage site featuring colonial architecture and coastal views.',
                        'location': 'Southern Province, Sri Lanka',
                        'best_time': 'Sunset for beautiful views, avoid monsoon season',
                        'highlights': ['Dutch Reformed Church', 'Maritime Museum', 'Lighthouse', 'Fort walls'],
                        'tips': ['Walk the fort walls at sunset', 'Visit the Maritime Museum', 'Explore boutique shops']
                    }
                },
                'si': {
                    'sigiriya': {
                        'name': 'සීගිරිය',
                        'description': 'පුරාණ රාජ මාලිගාවක් සහ බලකොටුවක් වන මෙය විශාල ගල් තීරුවක් මත ඉදිකර ඇත. ලෝකයේ 8 වැනි ආශ්චර්‍යය ලෙස හැඳින්වේ.',
                        'location': 'මධ්‍යම පළාත, ශ්‍රී ලංකාව',
                        'best_time': 'බහුල ජනයා සහ උණුසුම වළක්වා ගැනීමට උදෑසන හෝ සවස් කාලය',
                        'entrance_fee': 'විදේශිකයින් සඳහා ඇමරිකානු ඩොලර් 30 ක් පමණ',
                        'highlights': ['සිංහ පාද ඇතුළුවීම', 'චිත්‍ර', 'ආදර්ශ දෙවිලි', 'රාජකීය උද්‍යාන'],
                        'tips': ['සුවපහසු සපත්තු පැළඳින්න', 'ජලය ගෙන එන්න', 'උදෑසන ගොස් බලන්න', 'ඉතිහාසය සඳහා මඟපෙන්වීම් ගන්න']
                    },
                    'kandy': {
                        'name': 'මහනුවර',
                        'description': 'ශ්‍රී ලංකාවේ සංස්කෘතික අගනුවර, ශ්‍රී දන්ත ධාතුන් වහන්සේගේ දේවාලය පිහිටා ඇත.',
                        'location': 'මධ්‍යම පළාත, ශ්‍රී ලංකාව',
                        'best_time': 'සෑම වර්ෂයකම, නමුත් පෙරහැර උත්සවය අතරතුර (ජූලි/අගෝස්තු)',
                        'highlights': ['ශ්‍රී දන්ත ධාතුන් වහන්සේගේ දේවාලය', 'රාජකීය උද්‍යාන', 'මහනුවර වැව', 'සංස්කෘතික නැටුම්'],
                        'tips': ['දේවාලයට ගිය විට ලැජ්ජාසනයෙන් ඇඳින්න', 'සංස්කෘතික නැටුම් නරඹන්න', 'පෙරහැර අතරතුර ගොස් බලන්න']
                    }
                },
                'ta': {
                    'sigiriya': {
                        'name': 'சிகிரியா',
                        'description': 'பழைய அரண்மனை மற்றும் கோட்டை வளாகம் ஒரு பெரிய பாறை நெடுவரிசையில் கட்டப்பட்டுள்ளது. உலகின் 8 வது அதிசயமாக அறியப்படுகிறது.',
                        'location': 'மத்திய மாகாணம், இலங்கை',
                        'best_time': 'கூட்டம் மற்றும் வெப்பத்தைத் தவிர்க்க காலை அல்லது மாலை',
                        'entrance_fee': 'வெளிநாட்டவர்களுக்கு தோராயமாக $30 அமெரிக்க டாலர்',
                        'highlights': ['சிங்க பாத நுழைவு', 'சுவர் ஓவியங்கள்', 'கண்ணாடி சுவர்', 'ராஜ பூங்காக்கள்'],
                        'tips': ['வசதியான காலணிகள் அணியுங்கள்', 'தண்ணீர் கொண்டு வாருங்கள்', 'காலையில் செல்லுங்கள்', 'வரலாற்றுக்கு வழிகாட்டியை நியமிக்கவும்']
                    }
                },
                'zh': {
                    'sigiriya': {
                        'name': '锡吉里耶',
                        'description': '锡吉里耶是一座宏伟的古代宫殿和堡垒建筑群，建在巨大的岩石柱上。被称为世界第八大奇迹。',
                        'location': '斯里兰卡中部省',
                        'best_time': '清晨或傍晚，避开人群和炎热',
                        'entrance_fee': '外国人约30美元',
                        'highlights': ['狮子爪入口', '壁画', '镜墙', '皇家花园'],
                        'tips': ['穿舒适的鞋子', '带水', '清晨参观', '雇导游了解历史']
                    },
                    'kandy': {
                        'name': '康提',
                        'description': '斯里兰卡的文化之都，拥有神圣的佛牙寺。',
                        'location': '斯里兰卡中部省',
                        'best_time': '全年，但最好在佩拉赫拉节期间（7月/8月）',
                        'highlights': ['佛牙寺', '皇家植物园', '康提湖', '文化表演'],
                        'tips': ['参观寺庙时穿着得体', '观看文化舞蹈表演', '在佩拉赫拉节期间参观']
                    }
                },
                'fr': {
                    'sigiriya': {
                        'name': 'Sigiriya',
                        'description': 'Ancien palais et complexe de forteresse construit sur une colonne rocheuse massive. Connu comme la 8ème merveille du monde.',
                        'location': 'Province centrale, Sri Lanka',
                        'best_time': 'Tôt le matin ou en fin d\'après-midi pour éviter la foule et la chaleur',
                        'entrance_fee': 'Environ 30 USD pour les étrangers',
                        'highlights': ['Entrée de la patte du lion', 'Peintures murales', 'Mur miroir', 'Jardins royaux'],
                        'tips': ['Portez des chaussures confortables', 'Apportez de l\'eau', 'Visitez tôt le matin', 'Engagez un guide pour l\'histoire']
                    },
                    'kandy': {
                        'name': 'Kandy',
                        'description': 'Capitale culturelle du Sri Lanka, abrite le Temple de la Dent Sacrée.',
                        'location': 'Province centrale, Sri Lanka',
                        'best_time': 'Toute l\'année, mais mieux pendant le festival Perahera (juillet/août)',
                        'highlights': ['Temple de la Dent Sacrée', 'Jardins botaniques royaux', 'Lac de Kandy', 'Spectacles culturels'],
                        'tips': ['Habillez-vous modestement pour les visites de temples', 'Assistez aux spectacles de danse culturelle', 'Visitez pendant Perahera']
                    }
                }
            },
            'food': {
                'en': {
                    'rice_and_curry': {
                        'name': 'Rice and Curry',
                        'description': 'Traditional Sri Lankan meal with rice and various curries.',
                        'ingredients': ['Rice', 'Fish curry', 'Chicken curry', 'Dhal', 'Vegetables'],
                        'best_places': ['Local restaurants', 'Guest houses', 'Home stays'],
                        'tips': ['Try with your hands for authentic experience', 'Ask for spice level preference']
                    },
                    'hoppers': {
                        'name': 'Hoppers (Appa)',
                        'description': 'Crispy, bowl-shaped pancakes made from rice flour and coconut milk.',
                        'ingredients': ['Rice flour', 'Coconut milk', 'Yeast', 'Sugar', 'Salt'],
                        'best_places': ['Street vendors', 'Local cafes', 'Traditional restaurants'],
                        'tips': ['Best eaten hot and fresh', 'Try with curry or chutney']
                    },
                    'kottu_roti': {
                        'name': 'Kottu Roti',
                        'description': 'Shredded flatbread stir-fried with vegetables, eggs, and spices.',
                        'ingredients': ['Roti bread', 'Vegetables', 'Eggs', 'Spices', 'Meat (optional)'],
                        'best_places': ['Street food stalls', 'Local restaurants'],
                        'tips': ['Very filling meal', 'Ask for your preferred spice level']
                    }
                },
                'si': {
                    'rice_and_curry': {
                        'name': 'බත් සහ කරවල',
                        'description': 'බත් සහ විවිධ කරවල සමඟ සම්ප්‍රදායික ශ්‍රී ලාංකීය ආහාර.',
                        'ingredients': ['බත්', 'මාළු කරවල', 'කුකුළු මස් කරවල', 'පරිප්පු', 'එළවළු'],
                        'best_places': ['ස්ථානීය අවන්හල්', 'ගෙවල්', 'නිවසේ රැඳී සිටීම'],
                        'tips': ['සත්‍ය අත්දැකීමක් සඳහා අත්වලින් උත්සාහ කරන්න', 'මසාල මට්ටම ගැන අසන්න']
                    }
                },
                'ta': {
                    'rice_and_curry': {
                        'name': 'சோறு மற்றும் குழம்பு',
                        'description': 'அரிசி மற்றும் பல்வேறு குழம்புகளுடன் பாரம்பரிய இலங்கை உணவு.',
                        'ingredients': ['அரிசி', 'மீன் குழம்பு', 'கோழி குழம்பு', 'தால்', 'காய்கறிகள்'],
                        'best_places': ['உள்ளூர் உணவகங்கள்', 'விருந்தோம்பல் வீடுகள்', 'வீட்டில் தங்குதல்'],
                        'tips': ['உண்மையான அனுபவத்திற்கு கைகளால் முயற்சிக்கவும்', 'மசாலா அளவு விருப்பத்தைக் கேள்வி']
                    }
                },
                'zh': {
                    'rice_and_curry': {
                        'name': '咖喱饭',
                        'description': '传统的斯里兰卡餐，配有米饭和各种咖喱。',
                        'ingredients': ['米饭', '鱼咖喱', '鸡肉咖喱', '豆子', '蔬菜'],
                        'best_places': ['当地餐厅', '民宿', '家庭旅馆'],
                        'tips': ['用手尝试以获得真实体验', '询问辣度偏好']
                    },
                    'hoppers': {
                        'name': '薄饼',
                        'description': '用米粉和椰奶制成的脆脆碗状煎饼。',
                        'ingredients': ['米粉', '椰奶', '酵母', '糖', '盐'],
                        'best_places': ['街头小贩', '当地咖啡馆', '传统餐厅'],
                        'tips': ['最好趁热新鲜食用', '配咖喱或酸辣酱']
                    }
                },
                'fr': {
                    'rice_and_curry': {
                        'name': 'Riz et Curry',
                        'description': 'Repas traditionnel sri-lankais avec du riz et divers currys.',
                        'ingredients': ['Riz', 'Curry de poisson', 'Curry de poulet', 'Dhal', 'Légumes'],
                        'best_places': ['Restaurants locaux', 'Maisons d\'hôtes', 'Séjours chez l\'habitant'],
                        'tips': ['Essayez avec vos mains pour une expérience authentique', 'Demandez le niveau d\'épices préféré']
                    },
                    'hoppers': {
                        'name': 'Hoppers (Appa)',
                        'description': 'Crêpes croustillantes en forme de bol faites de farine de riz et de lait de coco.',
                        'ingredients': ['Farine de riz', 'Lait de coco', 'Levure', 'Sucre', 'Sel'],
                        'best_places': ['Vendeurs de rue', 'Cafés locaux', 'Restaurants traditionnels'],
                        'tips': ['Meilleur mangé chaud et frais', 'Essayez avec du curry ou du chutney']
                    }
                }
            },
            'culture': {
                'en': {
                    'greeting': {
                        'custom': 'Say "Ayubowan" (meaning "May you live long") with palms together',
                        'meaning': 'Traditional greeting showing respect and good wishes',
                        'when_to_use': 'Meeting people, entering temples, formal occasions',
                        'variations': ['Ayubowan', 'Vanakkam (Tamil)', 'Hello (English)']
                    },
                    'temple_etiquette': {
                        'dress_code': 'Modest clothing, cover shoulders and knees',
                        'shoes': 'Remove shoes before entering',
                        'behavior': 'Quiet and respectful, no photography in some areas',
                        'offerings': 'Flowers, incense, or small donations welcome'
                    },
                    'festivals': {
                        'sinhala_new_year': {
                            'name': 'Sinhala and Tamil New Year (April)',
                            'description': 'Major cultural celebration with traditional games and customs',
                            'activities': ['Traditional games', 'Family gatherings', 'Special meals', 'Rituals']
                        },
                        'perahera': {
                            'name': 'Esala Perahera (July/August)',
                            'description': 'Grand procession in Kandy with elephants and dancers',
                            'activities': ['Elephant parade', 'Traditional dances', 'Cultural performances', 'Religious ceremonies']
                        }
                    }
                },
                'si': {
                    'greeting': {
                        'custom': '"ආයුබෝවන්" (ඔබ දිගු කලක් ජීවත් වේවා යන අර්ථය) අත් දෙක එකට තබා කියන්න',
                        'meaning': 'ගෞරවය සහ යහපත් ආශිර්වාද පෙන්වන සම්ප්‍රදායික පිළිගැනීම',
                        'when_to_use': 'මිනිසුන් හමුවීම, දේවාලවලට ඇතුළු වීම, විධිමත් අවස්ථා',
                        'variations': ['ආයුබෝවන්', 'வணக்கம் (දෙමළ)', 'Hello (ඉංග්‍රීසි)']
                    }
                },
                'ta': {
                    'greeting': {
                        'custom': '"வணக்கம்" (நீங்கள் நீண்ட காலம் வாழ்க என்பது பொருள்) கைகளை சேர்த்து கூறுங்கள்',
                        'meaning': 'மரியாதை மற்றும் நல்ல வாழ்த்துக்களைக் காட்டும் பாரம்பரிய வணக்கம்',
                        'when_to_use': 'மக்களை சந்திக்கும்போது, கோவில்களுக்குள் செல்லும்போது, முறையான சந்தர்ப்பங்களில்',
                        'variations': ['வணக்கம்', 'ආයුබෝවන් (සිංහල)', 'Hello (ஆங்கிலம்)']
                    }
                },
                'zh': {
                    'greeting': {
                        'custom': '说"阿育布万"（意为"愿你长寿"），双手合十',
                        'meaning': '表示尊重和美好祝愿的传统问候',
                        'when_to_use': '见面时、进入寺庙时、正式场合',
                        'variations': ['阿育布万', 'வணக்கம் (泰米尔语)', 'Hello (英语)']
                    },
                    'temple_etiquette': {
                        'dress_code': '穿着得体，遮盖肩膀和膝盖',
                        'shoes': '进入前脱鞋',
                        'behavior': '安静恭敬，某些区域禁止拍照',
                        'offerings': '欢迎献花、香火或小额捐赠'
                    }
                },
                'fr': {
                    'greeting': {
                        'custom': 'Dites "Ayubowan" (signifiant "Puissiez-vous vivre longtemps") avec les paumes jointes',
                        'meaning': 'Salutation traditionnelle montrant le respect et les bons vœux',
                        'when_to_use': 'Rencontrer des gens, entrer dans les temples, occasions formelles',
                        'variations': ['Ayubowan', 'வணக்கம் (Tamoul)', 'Hello (Anglais)']
                    },
                    'temple_etiquette': {
                        'dress_code': 'Vêtements modestes, couvrir les épaules et les genoux',
                        'shoes': 'Retirer les chaussures avant d\'entrer',
                        'behavior': 'Silencieux et respectueux, pas de photographie dans certaines zones',
                        'offerings': 'Fleurs, encens ou petits dons bienvenus'
                    }
                }
            },
            'transport': {
                'en': {
                    'buses': {
                        'description': 'Public bus service covering most of the country',
                        'cost': 'Very cheap (Rs. 20-200 depending on distance)',
                        'tips': ['Have exact change ready', 'Buses can be crowded', 'Ask locals for routes'],
                        'routes': ['Colombo to Kandy', 'Kandy to Sigiriya', 'Colombo to Galle']
                    },
                    'trains': {
                        'description': 'Scenic train journeys, especially the Kandy to Ella route',
                        'cost': 'Affordable (Rs. 50-500 depending on class and distance)',
                        'tips': ['Book 2nd or 3rd class for best views', 'Bring snacks and water', 'Arrive early for good seats'],
                        'scenic_routes': ['Kandy to Ella', 'Colombo to Kandy', 'Colombo to Galle']
                    },
                    'tuk_tuks': {
                        'description': 'Three-wheeled taxis, good for short distances',
                        'cost': 'Negotiable (Rs. 100-500 for short trips)',
                        'tips': ['Always negotiate price before getting in', 'Use meter if available', 'Good for airport transfers'],
                        'best_for': ['Airport transfers', 'City tours', 'Short distances']
                    }
                },
                'si': {
                    'buses': {
                        'description': 'රටේ බොහෝ ප්‍රදේශ ආවරණය කරන පොදු බස් සේවාව',
                        'cost': 'ඉතා ලාභදායී (දුර අනුව රු. 20-200)',
                        'tips': ['නිවැරදි මුදල් සූදානම් කර තබන්න', 'බස් බහුල විය හැකිය', 'මාර්ග සඳහා උද්‍යෝගිකයින්ගෙන් අසන්න'],
                        'routes': ['කොළඹ සිට මහනුවර', 'මහනුවර සිට සීගිරිය', 'කොළඹ සිට ගාල්ල']
                    }
                },
                'ta': {
                    'buses': {
                        'description': 'நாட்டின் பெரும்பாலான பகுதிகளை உள்ளடக்கிய பொது பஸ் சேவை',
                        'cost': 'மிகவும் மலிவானது (தூரத்தைப் பொறுத்து ரூ. 20-200)',
                        'tips': ['சரியான மாற்றத்தை தயாராக வைக்கவும்', 'பஸ்கள் நெரிசலாக இருக்கலாம்', 'வழிகளுக்கு உள்ளூர் மக்களிடம் கேள்விப்படவும்'],
                        'routes': ['கொழும்பு முதல் கண்டி', 'கண்டி முதல் சிகிரியா', 'கொழும்பு முதல் காலி']
                    }
                }
            },
            'accommodation': {
                'en': {
                    'hotels': {
                        'description': 'Range from budget to luxury hotels',
                        'price_range': 'Budget: $20-50, Mid-range: $50-150, Luxury: $150+',
                        'best_areas': ['Colombo Fort', 'Galle Face', 'Mount Lavinia', 'Negombo'],
                        'tips': ['Book in advance during peak season', 'Check for package deals', 'Read reviews carefully']
                    },
                    'guesthouses': {
                        'description': 'Family-run accommodations, more personal experience',
                        'price_range': '$15-40 per night',
                        'best_areas': ['Kandy', 'Galle', 'Sigiriya', 'Ella'],
                        'tips': ['Book directly with owners', 'Ask about meals', 'Great for cultural exchange']
                    },
                    'homestays': {
                        'description': 'Stay with local families, authentic cultural experience',
                        'price_range': '$10-30 per night including meals',
                        'best_areas': ['Rural villages', 'Tea estates', 'Coastal communities'],
                        'tips': ['Respect house rules', 'Participate in family activities', 'Learn local customs']
                    }
                },
                'si': {
                    'hotels': {
                        'description': 'අයවැයේ සිට විලාසිතා හෝටල් දක්වා පරාසය',
                        'price_range': 'අයවැය: $20-50, මධ්‍යම පන්තිය: $50-150, විලාසිතා: $150+',
                        'best_areas': ['කොළඹ කොටුව', 'ගාල්ල මුහුණත', 'මවුන්ට් ලැවිනියා', 'නෙගොම්බෝ'],
                        'tips': ['උච්චතම සෘතුවේ කලින් වෙන් කර ගන්න', 'පැකේජ ගනුදෙනු සඳහා පරීක්ෂා කරන්න', 'සමාලෝචන කාරfullyජ්‍යව කියවන්න']
                    }
                }
            }
        }
    
    def get_response(self, intent: str, language: str, entities: List[Dict] = None) -> str:
        """
        Get a response based on intent and language.
        
        Args:
            intent: The detected intent
            language: Language code ('en', 'si', 'ta')
            entities: Extracted entities from user message
            
        Returns:
            Response text in the specified language
        """
        try:
            if intent == 'greeting':
                return self._get_greeting_response(language)
            elif intent == 'attraction_info':
                return self._get_attraction_response(language, entities)
            elif intent == 'food_info':
                return self._get_food_response(language, entities)
            elif intent == 'culture_info':
                return self._get_culture_response(language, entities)
            elif intent == 'transport_info':
                return self._get_transport_response(language, entities)
            elif intent == 'accommodation_info':
                return self._get_accommodation_response(language, entities)
            elif intent == 'goodbye':
                return self._get_goodbye_response(language)
            else:
                return self._get_fallback_response(language)
                
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return self._get_error_response(language)
    
    def _get_greeting_response(self, language: str) -> str:
        """Get greeting response in specified language."""
        greetings = {
            'en': "Ayubowan! Welcome to Sri Lanka! I'm your virtual tour guide. How can I help you explore this beautiful island today?",
            'si': "ආයුබෝවන්! ශ්‍රී ලංකාවට සාදරයෙන් පිළිගනිමු! මම ඔබේ අතථ්‍ය සංචාරක මඟපෙන්වීම් කරන්නෙමි. අද මම ඔබට මෙම සුන්දර දිවයින ගවේෂණය කිරීමට කෙසේ උදව් කළ හැකිද?",
            'ta': "வணக்கம்! இலங்கைக்கு வரவேற்கிறோம்! நான் உங்கள் மெய்நிகர் சுற்றுலா வழிகாட்டி. இன்று இந்த அழகான தீவை ஆராய்ந்து கொள்ள நான் உங்களுக்கு எப்படி உதவ முடியும்?"
        }
        return greetings.get(language, greetings['en'])
    
    def _get_attraction_response(self, language: str, entities: List[Dict]) -> str:
        """Get attraction information response."""
        if not entities:
            return self._get_attraction_list(language)
        
        # Extract attraction name from entities
        attraction_name = None
        for entity in entities:
            if entity.get('type') == 'attraction':
                attraction_name = entity.get('value', '').lower()
                break
        
        if not attraction_name:
            return self._get_attraction_list(language)
        
        # Get specific attraction info
        for lang_code in [language, 'en']:  # Fallback to English if language not available
            if lang_code in self.knowledge['attractions']:
                for key, info in self.knowledge['attractions'][lang_code].items():
                    if attraction_name in key or key in attraction_name:
                        return self._format_attraction_info(info, lang_code)
        
        return self._get_attraction_not_found(language, attraction_name)
    
    def _get_food_response(self, language: str, entities: List[Dict]) -> str:
        """Get food information response."""
        if not entities:
            return self._get_food_list(language)
        
        # Extract food name from entities
        food_name = None
        for entity in entities:
            if entity.get('type') == 'food':
                food_name = entity.get('value', '').lower()
                break
        
        if not food_name:
            return self._get_food_list(language)
        
        # Get specific food info
        for lang_code in [language, 'en']:
            if lang_code in self.knowledge['food']:
                for key, info in self.knowledge['food'][lang_code].items():
                    if food_name in key or key in food_name:
                        return self._format_food_info(info, lang_code)
        
        return self._get_food_not_found(language, food_name)
    
    def _get_culture_response(self, language: str, entities: List[Dict]) -> str:
        """Get cultural information response."""
        if not entities:
            return self._get_culture_overview(language)
        
        # Extract culture topic from entities
        topic = None
        for entity in entities:
            if entity.get('type') == 'culture_topic':
                topic = entity.get('value', '').lower()
                break
        
        if not topic:
            return self._get_culture_overview(language)
        
        # Get specific culture info
        for lang_code in [language, 'en']:
            if lang_code in self.knowledge['culture']:
                for key, info in self.knowledge['culture'][lang_code].items():
                    if topic in key or key in topic:
                        return self._format_culture_info(info, lang_code)
        
        return self._get_culture_overview(language)
    
    def _get_transport_response(self, language: str, entities: List[Dict]) -> str:
        """Get transport information response."""
        if not entities:
            return self._get_transport_overview(language)
        
        # Extract transport type from entities
        transport_type = None
        for entity in entities:
            if entity.get('type') == 'transport_type':
                transport_type = entity.get('value', '').lower()
                break
        
        if not transport_type:
            return self._get_transport_overview(language)
        
        # Get specific transport info
        for lang_code in [language, 'en']:
            if lang_code in self.knowledge['transport']:
                for key, info in self.knowledge['transport'][lang_code].items():
                    if transport_type in key or key in transport_type:
                        return self._format_transport_info(info, lang_code)
        
        return self._get_transport_overview(language)
    
    def _get_accommodation_response(self, language: str, entities: List[Dict]) -> str:
        """Get accommodation information response."""
        if not entities:
            return self._get_accommodation_overview(language)
        
        # Extract accommodation type from entities
        acc_type = None
        for entity in entities:
            if entity.get('type') == 'accommodation_type':
                acc_type = entity.get('value', '').lower()
                break
        
        if not acc_type:
            return self._get_accommodation_overview(language)
        
        # Get specific accommodation info
        for lang_code in [language, 'en']:
            if lang_code in self.knowledge['accommodation']:
                for key, info in self.knowledge['accommodation'][lang_code].items():
                    if acc_type in key or key in acc_type:
                        return self._format_accommodation_info(info, lang_code)
        
        return self._get_accommodation_overview(language)
    
    def _get_goodbye_response(self, language: str) -> str:
        """Get goodbye response in specified language."""
        goodbyes = {
            'en': "Thank you for exploring Sri Lanka with me! Have a wonderful journey and come back soon. Ayubowan!",
            'si': "මා සමඟ ශ්‍රී ලංකාව ගවේෂණය කළ ඔබට ස්තූතියි! ඔබට අපූරු ගමනක් ලැබේවා, ඉක්මනින් නැවත එන්න. ආයුබෝවන්!",
            'ta': "என்னுடன் இலங்கையை ஆராய்ந்ததற்கு நன்றி! உங்களுக்கு அருமையான பயணம் கிடைக்கட்டும், விரைவில் திரும்பி வாருங்கள். வணக்கம்!"
        }
        return goodbyes.get(language, goodbyes['en'])
    
    def _get_fallback_response(self, language: str) -> str:
        """Get fallback response when intent is not recognized."""
        fallbacks = {
            'en': "I'm not sure I understood that. Could you please ask about attractions, food, culture, transport, or accommodation in Sri Lanka?",
            'si': "මට එය තේරුම්ගත නොහැකිය. කරුණාකර ශ්‍රී ලංකාවේ සංචාරක ස්ථාන, ආහාර, සංස්කෘතිය, ප්‍රවාහන හෝ නවාතැන් ගැන අසන්න?",
            'ta': "அதை நான் புரிந்துகொள்ளவில்லை. தயவுசெய்து இலங்கையின் சுற்றுலா இடங்கள், உணவு, கலாச்சாரம், போக்குவரத்து அல்லது வசிப்பிடம் பற்றி கேள்விப்படவும்?"
        }
        return fallbacks.get(language, fallbacks['en'])
    
    def _get_error_response(self, language: str) -> str:
        """Get error response when something goes wrong."""
        errors = {
            'en': "I apologize, but I'm having some technical difficulties. Please try asking your question again.",
            'si': "මට සමාවෙන්න, නමුත් මට තාක්ෂණික ගැටළු ඇත. කරුණාකර ඔබේ ප්‍රශ්නය නැවත අසන්න.",
            'ta': "மன்னிக்கவும், ஆனால் எனக்கு சில தொழில்நுட்ப சிக்கல்கள் உள்ளன. தயவுசெய்து உங்கள் கேள்வியை மீண்டும் கேள்விப்படுத்தவும்."
        }
        return errors.get(language, errors['en'])
    
    # Helper methods for formatting responses
    def _format_attraction_info(self, info: Dict, language: str) -> str:
        """Format attraction information into a readable response."""
        if language == 'en':
            return f"{info['name']}: {info['description']} Located in {info['location']}. Best time to visit: {info['best_time']}. Highlights include: {', '.join(info['highlights'])}. Tips: {', '.join(info['tips'])}"
        else:
            # For Sinhala and Tamil, return the description directly
            return f"{info['name']}: {info['description']}"
    
    def _format_food_info(self, info: Dict, language: str) -> str:
        """Format food information into a readable response."""
        if language == 'en':
            return f"{info['name']}: {info['description']} Best places to try: {', '.join(info['best_places'])}. Tips: {', '.join(info['tips'])}"
        else:
            return f"{info['name']}: {info['description']}"
    
    def _format_culture_info(self, info: Dict, language: str) -> str:
        """Format culture information into a readable response."""
        if language == 'en':
            if 'custom' in info:
                return f"{info['custom']}: {info['gesture']} Use when: {info['when_to_use']}. Tips: {', '.join(info['tips'])}"
            else:
                return str(info)
        else:
            return str(info)
    
    def _format_transport_info(self, info: Dict, language: str) -> str:
        """Format transport information into a readable response."""
        if language == 'en':
            return f"{info['description']} Cost: {info['cost']}. Tips: {', '.join(info['tips'])}"
        else:
            return info['description']
    
    def _format_accommodation_info(self, info: Dict, language: str) -> str:
        """Format accommodation information into a readable response."""
        if language == 'en':
            return f"{info['description']} Price range: {info['price_range']}. Best areas: {', '.join(info['best_areas'])}. Tips: {', '.join(info['tips'])}"
        else:
            return info['description']
    
    # List and overview methods
    def _get_attraction_list(self, language: str) -> str:
        """Get list of attractions."""
        if language == 'en':
            attractions = list(self.knowledge['attractions']['en'].keys())
            return f"Popular attractions in Sri Lanka include: {', '.join(attractions)}. Which one would you like to know more about?"
        else:
            return self._get_fallback_response(language)
    
    def _get_food_list(self, language: str) -> str:
        """Get list of foods."""
        if language == 'en':
            foods = list(self.knowledge['food']['en'].keys())
            return f"Popular Sri Lankan foods include: {', '.join(foods)}. Which one would you like to know more about?"
        else:
            return self._get_fallback_response(language)
    
    def _get_culture_overview(self, language: str) -> str:
        """Get cultural overview."""
        if language == 'en':
            return "Sri Lankan culture is rich and diverse. I can tell you about greetings, temple etiquette, festivals, and customs. What would you like to know?"
        else:
            return self._get_fallback_response(language)
    
    def _get_transport_overview(self, language: str) -> str:
        """Get transport overview."""
        if language == 'en':
            return "Sri Lanka has various transport options: buses, trains, tuk-tuks, and taxis. Which mode of transport would you like to know more about?"
        else:
            return self._get_fallback_response(language)
    
    def _get_accommodation_overview(self, language: str) -> str:
        """Get accommodation overview."""
        if language == 'en':
            return "Sri Lanka offers various accommodation types: hotels, guesthouses, and homestays. Which type would you like to know more about?"
        else:
            return self._get_fallback_response(language)
    
    def _get_attraction_not_found(self, language: str, attraction: str) -> str:
        """Get response when attraction is not found."""
        if language == 'en':
            return f"I don't have specific information about {attraction}, but I can tell you about popular attractions like Sigiriya, Kandy, and Galle Fort. Which would you like to know about?"
        else:
            return self._get_fallback_response(language)
    
    def _get_food_not_found(self, language: str, food: str) -> str:
        """Get response when food is not found."""
        if language == 'en':
            return f"I don't have specific information about {food}, but I can tell you about popular Sri Lankan foods like rice and curry, hoppers, and kottu roti. Which would you like to know about?"
        else:
            return self._get_fallback_response(language)