from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3
import json
from langdetect import detect
import requests

class ActionDetectLanguage(Action):
    def name(self) -> Text:
        return "action_detect_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest message
        latest_message = tracker.latest_message.get('text', '')
        
        try:
            # Detect language
            detected_lang = detect(latest_message)
            
            # Map language codes to our supported languages
            lang_mapping = {
                'si': 'sinhala',
                'ta': 'tamil', 
                'en': 'english'
            }
            
            detected_language = lang_mapping.get(detected_lang, 'english')
            
            # Set the language slot
            return [SlotSet("language", detected_language)]
            
        except:
            # Default to English if detection fails
            return [SlotSet("language", "english")]

class ActionGetAttractionDetails(Action):
    def name(self) -> Text:
        return "action_get_attraction_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the attraction name from entities
        attraction_name = next((entity['value'] for entity in tracker.latest_message['entities'] 
                              if entity['entity'] == 'attraction_name'), None)
        
        if not attraction_name:
            dispatcher.utter_message(text="Which attraction would you like to know about?")
            return []
        
        # Database query for attraction details
        attraction_details = self.get_attraction_from_db(attraction_name)
        
        if attraction_details:
            response = f"**{attraction_details['name']}**\n\n"
            response += f"**Location:** {attraction_details['location']}\n"
            response += f"**Description:** {attraction_details['description']}\n"
            response += f"**Best Time to Visit:** {attraction_details['best_time']}\n"
            response += f"**Entry Fee:** {attraction_details['entry_fee']}\n"
            response += f"**How to Get There:** {attraction_details['how_to_reach']}"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"I don't have detailed information about {attraction_name}. Please ask about popular attractions like Sigiriya, Nuwara Eliya, Galle Fort, or Yala National Park.")
        
        return []

    def get_attraction_from_db(self, attraction_name: str) -> Dict:
        # Sample data - in production, this would come from a database
        attractions = {
            "sigiriya": {
                "name": "Sigiriya (Lion Rock)",
                "location": "Central Province, Sri Lanka",
                "description": "Ancient palace and fortress complex built on a massive rock column. A UNESCO World Heritage site featuring stunning frescoes and the famous Lion's Paw entrance.",
                "best_time": "December to April (dry season)",
                "entry_fee": "Approximately $30 USD",
                "how_to_reach": "Take a bus or train from Colombo to Dambulla, then a tuk-tuk to Sigiriya. About 4-5 hours from Colombo."
            },
            "nuwara eliya": {
                "name": "Nuwara Eliya",
                "location": "Central Province, Sri Lanka",
                "description": "Known as 'Little England', this hill country town features tea plantations, cool climate, and colonial architecture.",
                "best_time": "March to May (spring season)",
                "entry_fee": "Free (attractions may have separate fees)",
                "how_to_reach": "Take the scenic train from Colombo or Kandy. About 6-7 hours from Colombo by train."
            },
            "galle fort": {
                "name": "Galle Fort",
                "location": "Southern Province, Sri Lanka",
                "description": "A UNESCO World Heritage site featuring a 16th-century Portuguese fort with Dutch colonial architecture, boutique hotels, and charming streets.",
                "best_time": "November to April",
                "entry_fee": "Free to enter the fort",
                "how_to_reach": "Take a train or bus from Colombo. About 2-3 hours from Colombo."
            },
            "yala": {
                "name": "Yala National Park",
                "location": "Southern Province, Sri Lanka",
                "description": "Famous for leopard sightings and diverse wildlife including elephants, crocodiles, and hundreds of bird species.",
                "best_time": "February to July (best for wildlife viewing)",
                "entry_fee": "Approximately $15 USD for foreigners",
                "how_to_reach": "Take a bus to Tissamaharama, then arrange a safari jeep. About 6 hours from Colombo."
            }
        }
        
        return attractions.get(attraction_name.lower())

class ActionGetFoodDetails(Action):
    def name(self) -> Text:
        return "action_get_food_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        food_item = next((entity['value'] for entity in tracker.latest_message['entities'] 
                         if entity['entity'] == 'food_item'), None)
        
        if not food_item:
            # Provide general food information
            response = "**Popular Sri Lankan Dishes:**\n\n"
            response += "🍛 **Rice and Curry** - The national dish with various curries\n"
            response += "🥘 **Kottu Roti** - Shredded roti with vegetables and meat\n"
            response += "🥞 **Hoppers (Appa)** - Crispy rice flour pancakes\n"
            response += "🍜 **String Hoppers** - Rice flour noodles\n"
            response += "🍖 **Lamprais** - Rice and meat wrapped in banana leaf\n"
            response += "🥥 **Coconut Sambol** - Spicy coconut relish\n\n"
            response += "**Where to eat:** Try local restaurants, street food stalls, and hotel buffets for authentic Sri Lankan cuisine."
            
            dispatcher.utter_message(text=response)
        else:
            # Provide specific food item details
            food_details = self.get_food_from_db(food_item)
            if food_details:
                response = f"**{food_details['name']}**\n\n"
                response += f"**Description:** {food_details['description']}\n"
                response += f"**Ingredients:** {food_details['ingredients']}\n"
                response += f"**Where to find:** {food_details['where_to_find']}"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"I don't have specific information about {food_item}. Try asking about popular dishes like rice and curry, kottu roti, or hoppers.")
        
        return []

    def get_food_from_db(self, food_item: str) -> Dict:
        foods = {
            "rice and curry": {
                "name": "Rice and Curry",
                "description": "The national dish of Sri Lanka, featuring steamed rice served with various curries including vegetables, fish, chicken, or beef.",
                "ingredients": "Rice, coconut milk, spices, vegetables, meat or fish",
                "where_to_find": "Available in most restaurants and hotels throughout Sri Lanka"
            },
            "kottu roti": {
                "name": "Kottu Roti",
                "description": "A popular street food made by shredding roti bread and mixing it with vegetables, eggs, and meat on a hot griddle.",
                "ingredients": "Roti bread, vegetables, eggs, chicken or beef, spices",
                "where_to_find": "Street food stalls, especially in Colombo and tourist areas"
            },
            "hoppers": {
                "name": "Hoppers (Appa)",
                "description": "Crispy, bowl-shaped pancakes made from rice flour and coconut milk, often served with curry or sambol.",
                "ingredients": "Rice flour, coconut milk, yeast, salt",
                "where_to_find": "Breakfast at hotels, street food stalls, and traditional restaurants"
            }
        }
        
        return foods.get(food_item.lower())

class ActionGetTransportDetails(Action):
    def name(self) -> Text:
        return "action_get_transport_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        transport_mode = next((entity['value'] for entity in tracker.latest_message['entities'] 
                              if entity['entity'] == 'transport_mode'), None)
        
        if not transport_mode:
            # Provide general transport information
            response = "**Transportation Options in Sri Lanka:**\n\n"
            response += "🚂 **Trains** - Scenic and affordable, connect major cities\n"
            response += "🚌 **Buses** - Extensive network, very cheap, can be crowded\n"
            response += "🚕 **Taxis/Tuk-tuks** - Convenient for short distances\n"
            response += "🚗 **Rental Cars** - Available but driving can be challenging\n"
            response += "✈️ **Domestic Flights** - Limited routes, mainly to Jaffna\n\n"
            response += "**Tips:** Trains are recommended for scenic routes like Colombo to Kandy or Nuwara Eliya."
            
            dispatcher.utter_message(text=response)
        else:
            # Provide specific transport mode details
            transport_details = self.get_transport_from_db(transport_mode)
            if transport_details:
                response = f"**{transport_details['name']}**\n\n"
                response += f"**Description:** {transport_details['description']}\n"
                response += f"**Cost:** {transport_details['cost']}\n"
                response += f"**Availability:** {transport_details['availability']}\n"
                response += f"**Tips:** {transport_details['tips']}"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"I don't have specific information about {transport_mode}. Try asking about trains, buses, or taxis.")
        
        return []

    def get_transport_from_db(self, transport_mode: str) -> Dict:
        transport = {
            "train": {
                "name": "Trains",
                "description": "Sri Lanka Railways operates an extensive network connecting major cities and towns.",
                "cost": "Very affordable, 2nd class tickets from $1-5 USD",
                "availability": "Regular services between major cities, book in advance for popular routes",
                "tips": "Book 1st or 2nd class for comfort, 3rd class can be very crowded"
            },
            "bus": {
                "name": "Buses",
                "description": "Extensive bus network covering almost every part of the country.",
                "cost": "Very cheap, typically $0.50-2 USD for most routes",
                "availability": "Frequent services, no advance booking needed",
                "tips": "Can be crowded and hot, bring water and patience"
            },
            "taxi": {
                "name": "Taxis and Tuk-tuks",
                "description": "Convenient for short distances and airport transfers.",
                "cost": "Tuk-tuks: $1-5 USD, Taxis: $5-20 USD depending on distance",
                "availability": "Readily available in cities and tourist areas",
                "tips": "Always negotiate the fare before getting in, tuk-tuks are cheaper than taxis"
            }
        }
        
        return transport.get(transport_mode.lower())

class ActionGetHotelDetails(Action):
    def name(self) -> Text:
        return "action_get_hotel_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        hotel_type = next((entity['value'] for entity in tracker.latest_message['entities'] 
                          if entity['entity'] == 'hotel_type'), None)
        
        city = next((entity['value'] for entity in tracker.latest_message['entities'] 
                    if entity['entity'] == 'city'), None)
        
        response = "**Accommodation Options in Sri Lanka:**\n\n"
        response += "🏨 **Luxury Hotels** - 5-star properties in Colombo, Kandy, and beach areas\n"
        response += "🏠 **Boutique Hotels** - Charming properties in Galle Fort and hill country\n"
        response += "🏡 **Guesthouses** - Family-run accommodations, great for cultural experience\n"
        response += "🏕️ **Eco-lodges** - Sustainable options near national parks\n"
        response += "🏨 **Budget Hotels** - Affordable options in all major cities\n\n"
        response += "**Booking Tips:**\n"
        response += "• Book in advance during peak season (December-April)\n"
        response += "• Popular booking sites: Booking.com, Agoda, Airbnb\n"
        response += "• Consider location - beach hotels vs city hotels\n"
        response += "• Check for air conditioning in hot areas"
        
        dispatcher.utter_message(text=response)
        return []

class ActionGetEmergencyContacts(Action):
    def name(self) -> Text:
        return "action_get_emergency_contacts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = "**Emergency Contact Numbers in Sri Lanka:**\n\n"
        response += "🚨 **General Emergency:** 119\n"
        response += "🚑 **Ambulance:** 110\n"
        response += "🚒 **Fire Services:** 111\n"
        response += "👮 **Tourist Police:** 011-242-1052\n"
        response += "🏥 **Colombo General Hospital:** 011-269-1111\n\n"
        response += "**Important Tips:**\n"
        response += "• Keep your embassy contact details handy\n"
        response += "• Tourist police speak English and can help with translation\n"
        response += "• Most hotels have 24/7 assistance\n"
        response += "• Consider travel insurance for medical emergencies"
        
        dispatcher.utter_message(text=response)
        return []