"""
Real-time APIs Integration Component

Integrates with external APIs to provide real-time tourism information
including weather, maps, events, and transportation data.
"""

import logging
import requests
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import time
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class APIStatus(Enum):
    """API service status enumeration."""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"


@dataclass
class APIResponse:
    """Standardized API response structure."""
    success: bool
    data: Any
    status: APIStatus
    timestamp: datetime
    error_message: Optional[str] = None
    rate_limit_info: Optional[Dict] = None


class RealTimeAPIsHandler:
    """
    Handles integration with external real-time APIs for tourism information.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the real-time APIs handler.
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config or {}
        
        # API configuration
        self.api_keys = {
            'google_maps': self.config.get('GOOGLE_MAPS_API_KEY'),
            'openweather': self.config.get('OPENWEATHER_API_KEY'),
            'currency': self.config.get('CURRENCY_API_KEY'),
            'events': self.config.get('EVENTS_API_KEY')
        }
        
        # API endpoints
        self.endpoints = {
            'google_maps': 'https://maps.googleapis.com/maps/api',
            'openweather': 'https://api.openweathermap.org/data/2.5',
            'currency': 'https://api.exchangerate-api.com/v4/latest',
            'events': 'https://api.eventbrite.com/v3'
        }
        
        # Rate limiting and caching
        self.rate_limits = {}
        self.cache = {}
        self.cache_duration = timedelta(minutes=15)  # 15 minutes cache
        
        # Service status
        self.service_status = {}
        
        logger.info("Real-time APIs Handler initialized successfully")
    
    def get_weather_info(self, location: str, language: str = 'en') -> APIResponse:
        """
        Get current weather information for a location.
        
        Args:
            location: City or location name
            language: Language for response
            
        Returns:
            APIResponse with weather data
        """
        try:
            # Check cache first
            cache_key = f"weather_{location}_{language}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return APIResponse(
                    success=True,
                    data=cached_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            
            # Check API availability
            if not self.api_keys['openweather']:
                return APIResponse(
                    success=False,
                    data=None,
                    status=APIStatus.UNAVAILABLE,
                    timestamp=datetime.now(),
                    error_message="OpenWeather API key not configured"
                )
            
            # Make API request
            url = f"{self.endpoints['openweather']}/weather"
            params = {
                'q': f"{location},LK",  # Sri Lanka
                'appid': self.api_keys['openweather'],
                'units': 'metric',
                'lang': self._get_weather_language_code(language)
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                weather_data = response.json()
                processed_data = self._process_weather_data(weather_data, language)
                
                # Cache the result
                self._cache_data(cache_key, processed_data)
                
                return APIResponse(
                    success=True,
                    data=processed_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            else:
                return APIResponse(
                    success=False,
                    data=None,
                    status=APIStatus.ERROR,
                    timestamp=datetime.now(),
                    error_message=f"Weather API error: {response.status_code}"
                )
                
        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message="Weather API request timeout"
            )
        except Exception as e:
            logger.error(f"Error getting weather info: {str(e)}")
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def get_directions(self, origin: str, destination: str, 
                      mode: str = 'driving', language: str = 'en') -> APIResponse:
        """
        Get directions between two locations.
        
        Args:
            origin: Starting location
            destination: End location
            mode: Travel mode (driving, walking, transit)
            language: Language for response
            
        Returns:
            APIResponse with directions data
        """
        try:
            # Check cache first
            cache_key = f"directions_{origin}_{destination}_{mode}_{language}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return APIResponse(
                    success=True,
                    data=cached_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            
            # Check API availability
            if not self.api_keys['google_maps']:
                return APIResponse(
                    success=False,
                    data=None,
                    status=APIStatus.UNAVAILABLE,
                    timestamp=datetime.now(),
                    error_message="Google Maps API key not configured"
                )
            
            # Make API request
            url = f"{self.endpoints['google_maps']}/directions/json"
            params = {
                'origin': origin,
                'destination': destination,
                'mode': mode,
                'key': self.api_keys['google_maps'],
                'language': self._get_maps_language_code(language),
                'region': 'lk'  # Sri Lanka
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                directions_data = response.json()
                
                if directions_data.get('status') == 'OK':
                    processed_data = self._process_directions_data(directions_data, language)
                    
                    # Cache the result
                    self._cache_data(cache_key, processed_data)
                    
                    return APIResponse(
                        success=True,
                        data=processed_data,
                        status=APIStatus.AVAILABLE,
                        timestamp=datetime.now()
                    )
                else:
                    return APIResponse(
                        success=False,
                        data=None,
                        status=APIStatus.ERROR,
                        timestamp=datetime.now(),
                        error_message=f"Directions API error: {directions_data.get('status')}"
                    )
            else:
                return APIResponse(
                    success=False,
                    data=None,
                    status=APIStatus.ERROR,
                    timestamp=datetime.now(),
                    error_message=f"Directions API error: {response.status_code}"
                )
                
        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message="Directions API request timeout"
            )
        except Exception as e:
            logger.error(f"Error getting directions: {str(e)}")
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def get_nearby_places(self, location: str, place_type: str, 
                          radius: int = 5000, language: str = 'en') -> APIResponse:
        """
        Get nearby places of interest.
        
        Args:
            location: Center location (lat,lng or place name)
            place_type: Type of place to search for
            radius: Search radius in meters
            language: Language for response
            
        Returns:
            APIResponse with places data
        """
        try:
            # Check cache first
            cache_key = f"places_{location}_{place_type}_{radius}_{language}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return APIResponse(
                    success=True,
                    data=cached_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            
            # Check API availability
            if not self.api_keys['google_maps']:
                return APIResponse(
                    success=False,
                    data=None,
                    status=APIStatus.UNAVAILABLE,
                    timestamp=datetime.now(),
                    error_message="Google Maps API key not configured"
                )
            
            # Make API request
            url = f"{self.endpoints['google_maps']}/place/nearbysearch/json"
            params = {
                'location': location,
                'radius': radius,
                'type': place_type,
                'key': self.api_keys['google_maps'],
                'language': self._get_maps_language_code(language)
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                places_data = response.json()
                
                if places_data.get('status') == 'OK':
                    processed_data = self._process_places_data(places_data, language)
                    
                    # Cache the result
                    self._cache_data(cache_key, processed_data)
                    
                    return APIResponse(
                        success=True,
                        data=processed_data,
                        status=APIStatus.AVAILABLE,
                        timestamp=datetime.now()
                    )
                else:
                    return APIResponse(
                        success=False,
                        data=None,
                        status=APIStatus.ERROR,
                        timestamp=datetime.now(),
                        error_message=f"Places API error: {places_data.get('status')}"
                    )
            else:
                return APIResponse(
                    success=False,
                    data=None,
                    status=APIStatus.ERROR,
                    timestamp=datetime.now(),
                    error_message=f"Places API error: {response.status_code}"
                )
                
        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message="Places API request timeout"
            )
        except Exception as e:
            logger.error(f"Error getting nearby places: {str(e)}")
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def get_currency_rate(self, base_currency: str = 'USD', 
                          target_currency: str = 'LKR') -> APIResponse:
        """
        Get current currency exchange rate.
        
        Args:
            base_currency: Base currency code
            target_currency: Target currency code
            
        Returns:
            APIResponse with currency data
        """
        try:
            # Check cache first
            cache_key = f"currency_{base_currency}_{target_currency}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return APIResponse(
                    success=True,
                    data=cached_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            
            # Make API request
            url = f"{self.endpoints['currency']}/{base_currency}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                currency_data = response.json()
                processed_data = self._process_currency_data(currency_data, base_currency, target_currency)
                
                # Cache the result (currency rates change frequently, shorter cache)
                self._cache_data(cache_key, processed_data, timedelta(minutes=5))
                
                return APIResponse(
                    success=True,
                    data=processed_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            else:
                return APIResponse(
                    success=False,
                    data=None,
                    status=APIStatus.ERROR,
                    timestamp=datetime.now(),
                    error_message=f"Currency API error: {response.status_code}"
                )
                
        except requests.exceptions.Timeout:
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message="Currency API request timeout"
            )
        except Exception as e:
            logger.error(f"Error getting currency rate: {str(e)}")
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def get_local_events(self, location: str, date_from: str = None, 
                         date_to: str = None, language: str = 'en') -> APIResponse:
        """
        Get local events and festivals.
        
        Args:
            location: Location to search for events
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            language: Language for response
            
        Returns:
            APIResponse with events data
        """
        try:
            # Check cache first
            cache_key = f"events_{location}_{date_from}_{date_to}_{language}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return APIResponse(
                    success=True,
                    data=cached_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            
            # For now, return simulated events data
            # In production, integrate with actual events API
            events_data = self._get_simulated_events(location, date_from, date_to, language)
            
            # Cache the result
            self._cache_data(cache_key, events_data)
            
            return APIResponse(
                success=True,
                data=events_data,
                status=APIStatus.AVAILABLE,
                timestamp=datetime.now()
            )
                
        except Exception as e:
            logger.error(f"Error getting local events: {str(e)}")
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def get_transport_info(self, origin: str, destination: str, 
                          transport_type: str = 'public', language: str = 'en') -> APIResponse:
        """
        Get public transport information.
        
        Args:
            origin: Starting location
            destination: End location
            transport_type: Type of transport (public, bus, train)
            language: Language for response
            
        Returns:
            APIResponse with transport data
        """
        try:
            # Check cache first
            cache_key = f"transport_{origin}_{destination}_{transport_type}_{language}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return APIResponse(
                    success=True,
                    data=cached_data,
                    status=APIStatus.AVAILABLE,
                    timestamp=datetime.now()
                )
            
            # For now, return simulated transport data
            # In production, integrate with actual transport APIs
            transport_data = self._get_simulated_transport(origin, destination, transport_type, language)
            
            # Cache the result
            self._cache_data(cache_key, transport_data)
            
            return APIResponse(
                success=True,
                data=transport_data,
                status=APIStatus.AVAILABLE,
                timestamp=datetime.now()
            )
                
        except Exception as e:
            logger.error(f"Error getting transport info: {str(e)}")
            return APIResponse(
                success=False,
                data=None,
                status=APIStatus.ERROR,
                timestamp=datetime.now(),
                error_message=str(e)
            )
    
    def _process_weather_data(self, weather_data: Dict, language: str) -> Dict:
        """Process raw weather data into user-friendly format."""
        try:
            main = weather_data.get('main', {})
            weather = weather_data.get('weather', [{}])[0]
            wind = weather_data.get('wind', {})
            
            # Get language-specific descriptions
            weather_descriptions = self._get_weather_descriptions(language)
            
            processed_data = {
                'location': weather_data.get('name', 'Unknown'),
                'temperature': {
                    'current': round(main.get('temp', 0), 1),
                    'feels_like': round(main.get('feels_like', 0), 1),
                    'min': round(main.get('temp_min', 0), 1),
                    'max': round(main.get('temp_max', 0), 1)
                },
                'humidity': main.get('humidity', 0),
                'pressure': main.get('pressure', 0),
                'wind': {
                    'speed': round(wind.get('speed', 0), 1),
                    'direction': wind.get('deg', 0)
                },
                'description': weather_descriptions.get(weather.get('id', 800), 'Unknown'),
                'icon': weather.get('icon', '01d'),
                'timestamp': datetime.now().isoformat()
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing weather data: {str(e)}")
            return {}
    
    def _process_directions_data(self, directions_data: Dict, language: str) -> Dict:
        """Process raw directions data into user-friendly format."""
        try:
            routes = directions_data.get('routes', [])
            if not routes:
                return {}
            
            route = routes[0]
            legs = route.get('legs', [])
            if not legs:
                return {}
            
            leg = legs[0]
            steps = leg.get('steps', [])
            
            # Get language-specific instructions
            instructions = self._get_direction_instructions(language)
            
            processed_data = {
                'origin': leg.get('start_address', ''),
                'destination': leg.get('end_address', ''),
                'distance': {
                    'text': leg.get('distance', {}).get('text', ''),
                    'value': leg.get('distance', {}).get('value', 0)
                },
                'duration': {
                    'text': leg.get('duration', {}).get('text', ''),
                    'value': leg.get('duration', {}).get('value', 0)
                },
                'steps': [
                    {
                        'instruction': step.get('html_instructions', ''),
                        'distance': step.get('distance', {}).get('text', ''),
                        'duration': step.get('duration', {}).get('text', ''),
                        'travel_mode': step.get('travel_mode', '')
                    }
                    for step in steps[:10]  # Limit to first 10 steps
                ],
                'summary': route.get('summary', ''),
                'warnings': route.get('warnings', [])
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing directions data: {str(e)}")
            return {}
    
    def _process_places_data(self, places_data: Dict, language: str) -> Dict:
        """Process raw places data into user-friendly format."""
        try:
            results = places_data.get('results', [])
            
            processed_places = []
            for place in results[:10]:  # Limit to first 10 places
                processed_place = {
                    'name': place.get('name', ''),
                    'address': place.get('vicinity', ''),
                    'rating': place.get('rating', 0),
                    'types': place.get('types', []),
                    'location': place.get('geometry', {}).get('location', {}),
                    'photos': place.get('photos', []),
                    'open_now': place.get('opening_hours', {}).get('open_now', None)
                }
                processed_places.append(processed_place)
            
            return {
                'places': processed_places,
                'total_results': len(results),
                'next_page_token': places_data.get('next_page_token', '')
            }
            
        except Exception as e:
            logger.error(f"Error processing places data: {str(e)}")
            return {}
    
    def _process_currency_data(self, currency_data: Dict, base: str, target: str) -> Dict:
        """Process raw currency data into user-friendly format."""
        try:
            rates = currency_data.get('rates', {})
            target_rate = rates.get(target, 0)
            
            return {
                'base_currency': base,
                'target_currency': target,
                'exchange_rate': target_rate,
                'last_updated': currency_data.get('time_last_updated_utc', ''),
                'rates': rates
            }
            
        except Exception as e:
            logger.error(f"Error processing currency data: {str(e)}")
            return {}
    
    def _get_simulated_events(self, location: str, date_from: str, 
                              date_to: str, language: str) -> Dict:
        """Get simulated events data for demonstration."""
        events = [
            {
                'name': 'Sinhala and Tamil New Year Festival',
                'name_si': 'සිංහල සහ දෙමළ අලුත් අවුරුද්ද උත්සවය',
                'name_ta': 'சிங்கள மற்றும் தமிழ் புத்தாண்டு திருவிழா',
                'description': 'Traditional New Year celebrations with cultural performances',
                'date': '2024-04-13',
                'location': 'Various locations across Sri Lanka',
                'type': 'Cultural Festival',
                'free': True
            },
            {
                'name': 'Esala Perahera',
                'name_si': 'එළාල පෙරහැර',
                'name_ta': 'எளளா பெரஹெர',
                'description': 'Grand procession in Kandy with elephants and traditional dancers',
                'date': '2024-07-20',
                'location': 'Kandy, Central Province',
                'type': 'Religious Festival',
                'free': True
            },
            {
                'name': 'Galle Literary Festival',
                'name_si': 'ගාල්ල සාහිත්‍ය උත්සවය',
                'name_ta': 'காலி இலக்கிய திருவிழா',
                'description': 'International literary festival in the historic Galle Fort',
                'date': '2024-01-25',
                'location': 'Galle Fort, Southern Province',
                'type': 'Literary Festival',
                'free': False
            }
        ]
        
        # Filter by location if specified
        if location and location.lower() != 'sri lanka':
            events = [e for e in events if location.lower() in e['location'].lower()]
        
        return {
            'events': events,
            'total_count': len(events),
            'location': location,
            'date_range': {'from': date_from, 'to': date_to}
        }
    
    def _get_simulated_transport(self, origin: str, destination: str, 
                                 transport_type: str, language: str) -> Dict:
        """Get simulated transport data for demonstration."""
        transport_options = [
            {
                'type': 'Bus',
                'type_si': 'බස්',
                'type_ta': 'பஸ்',
                'departure': '08:00',
                'arrival': '10:30',
                'duration': '2h 30m',
                'price': 'Rs. 150',
                'operator': 'Sri Lanka Transport Board',
                'stops': ['Colombo', 'Kandy', 'Matale']
            },
            {
                'type': 'Train',
                'type_si': 'දුම්රිය',
                'type_ta': 'ரயில்',
                'departure': '07:30',
                'arrival': '10:00',
                'duration': '2h 30m',
                'price': 'Rs. 200',
                'operator': 'Sri Lanka Railways',
                'stops': ['Colombo Fort', 'Kandy', 'Peradeniya']
            }
        ]
        
        return {
            'origin': origin,
            'destination': destination,
            'transport_type': transport_type,
            'options': transport_options,
            'total_options': len(transport_options)
        }
    
    def _get_weather_descriptions(self, language: str) -> Dict:
        """Get weather descriptions in different languages."""
        descriptions = {
            'en': {
                200: 'Thunderstorm with light rain',
                300: 'Light drizzle',
                500: 'Light rain',
                600: 'Light snow',
                700: 'Mist',
                800: 'Clear sky',
                801: 'Few clouds',
                802: 'Scattered clouds',
                803: 'Broken clouds',
                804: 'Overcast clouds'
            },
            'si': {
                200: 'සැහැල්ලු වැසි සමඟ ගිගිරිම',
                300: 'සැහැල්ලු වැසි',
                500: 'සැහැල්ලු වැසි',
                600: 'සැහැල්ලු හිම',
                700: 'ඝන',
                800: 'පැහැදිලි ආකාශය',
                801: 'ස්වල්ප වලාකුළු',
                802: 'විසිරුණු වලාකුළු',
                803: 'බිඳුණු වලාකුළු',
                804: 'වැසි වලාකුළු'
            },
            'ta': {
                200: 'இலேசான மழையுடன் இடி',
                300: 'இலேசான தூறல்',
                500: 'இலேசான மழை',
                600: 'இலேசான பனி',
                700: 'மூடுபனி',
                800: 'தெளிவான வானம்',
                801: 'சில மேகங்கள்',
                802: 'சிதறிய மேகங்கள்',
                803: 'உடைந்த மேகங்கள்',
                804: 'மேகமூட்டம்'
            }
        }
        
        return descriptions.get(language, descriptions['en'])
    
    def _get_direction_instructions(self, language: str) -> Dict:
        """Get direction instructions in different languages."""
        instructions = {
            'en': {
                'turn_left': 'Turn left',
                'turn_right': 'Turn right',
                'go_straight': 'Go straight',
                'u_turn': 'Make a U-turn',
                'merge': 'Merge onto',
                'exit': 'Exit onto'
            },
            'si': {
                'turn_left': 'වමට හැරෙන්න',
                'turn_right': 'දකුණට හැරෙන්න',
                'go_straight': 'සෘජුව යන්න',
                'u_turn': 'U-හැරීමක් කරන්න',
                'merge': 'එකතු වන්න',
                'exit': 'පිටවන්න'
            },
            'ta': {
                'turn_left': 'இடதுபுறம் திரும்பவும்',
                'turn_right': 'வலதுபுறம் திரும்பவும்',
                'go_straight': 'நேராக செல்லவும்',
                'u_turn': 'U-திருப்பம் செய்யவும்',
                'merge': 'இணைவதற்கு',
                'exit': 'வெளியேற'
            }
        }
        
        return instructions.get(language, instructions['en'])
    
    def _get_weather_language_code(self, language: str) -> str:
        """Convert chatbot language code to OpenWeather language code."""
        language_map = {
            'en': 'en',
            'si': 'en',  # OpenWeather doesn't support Sinhala
            'ta': 'en'   # OpenWeather doesn't support Tamil
        }
        return language_map.get(language, 'en')
    
    def _get_maps_language_code(self, language: str) -> str:
        """Convert chatbot language code to Google Maps language code."""
        language_map = {
            'en': 'en',
            'si': 'si',  # Google Maps supports Sinhala
            'ta': 'ta'   # Google Maps supports Tamil
        }
        return language_map.get(language, 'en')
    
    def _get_cached_data(self, cache_key: str) -> Optional[Any]:
        """Get data from cache if available and not expired."""
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            if datetime.now() - cached_item['timestamp'] < cached_item['duration']:
                return cached_item['data']
            else:
                # Remove expired cache item
                del self.cache[cache_key]
        return None
    
    def _cache_data(self, cache_key: str, data: Any, 
                    duration: timedelta = None) -> None:
        """Cache data with specified duration."""
        if duration is None:
            duration = self.cache_duration
        
        self.cache[cache_key] = {
            'data': data,
            'timestamp': datetime.now(),
            'duration': duration
        }
        
        # Limit cache size
        if len(self.cache) > 100:
            # Remove oldest items
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
    
    def get_api_status(self) -> Dict:
        """Get status of all API services."""
        return {
            'google_maps': {
                'available': bool(self.api_keys['google_maps']),
                'status': APIStatus.AVAILABLE if self.api_keys['google_maps'] else APIStatus.UNAVAILABLE
            },
            'openweather': {
                'available': bool(self.api_keys['openweather']),
                'status': APIStatus.AVAILABLE if self.api_keys['openweather'] else APIStatus.UNAVAILABLE
            },
            'currency': {
                'available': True,  # Free API
                'status': APIStatus.AVAILABLE
            },
            'events': {
                'available': True,  # Simulated data
                'status': APIStatus.AVAILABLE
            },
            'transport': {
                'available': True,  # Simulated data
                'status': APIStatus.AVAILABLE
            }
        }
    
    def cleanup_cache(self):
        """Clean up expired cache items."""
        current_time = datetime.now()
        expired_keys = [
            key for key, item in self.cache.items()
            if current_time - item['timestamp'] > item['duration']
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache items")
    
    def get_handler_stats(self) -> Dict:
        """Get statistics about the API handler."""
        return {
            'api_keys_configured': sum(1 for key in self.api_keys.values() if key),
            'cache_size': len(self.cache),
            'cache_duration_minutes': self.cache_duration.total_seconds() / 60,
            'service_status': self.get_api_status(),
            'endpoints': self.endpoints
        }