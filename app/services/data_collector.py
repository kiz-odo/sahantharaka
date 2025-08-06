import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import logging
from app import db
from app.models import TouristArrival, TouristSource, Destination, Hotel, Booking, Occupancy, Revenue
from config import Config

logger = logging.getLogger(__name__)

class DataCollector:
    """Service for collecting tourism data from various sources"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        
    def collect_tourist_arrivals(self, start_date=None, end_date=None):
        """Collect tourist arrival data"""
        try:
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # In a real implementation, this would fetch from SLTDA API or airport data
            # For now, we'll generate simulated data
            arrivals_data = self._generate_simulated_arrivals(start_date, end_date)
            
            # Save to database
            for arrival in arrivals_data:
                self._save_tourist_arrival(arrival)
            
            logger.info(f"Collected {len(arrivals_data)} tourist arrival records")
            return len(arrivals_data)
            
        except Exception as e:
            logger.error(f"Error collecting tourist arrivals: {str(e)}")
            return 0
    
    def collect_hotel_data(self):
        """Collect hotel booking and occupancy data"""
        try:
            # Generate simulated hotel data
            hotels_data = self._generate_simulated_hotels()
            bookings_data = self._generate_simulated_bookings()
            occupancy_data = self._generate_simulated_occupancy()
            
            # Save to database
            for hotel in hotels_data:
                self._save_hotel(hotel)
            
            for booking in bookings_data:
                self._save_booking(booking)
            
            for occupancy in occupancy_data:
                self._save_occupancy(occupancy)
            
            logger.info(f"Collected hotel data: {len(hotels_data)} hotels, {len(bookings_data)} bookings, {len(occupancy_data)} occupancy records")
            return len(hotels_data) + len(bookings_data) + len(occupancy_data)
            
        except Exception as e:
            logger.error(f"Error collecting hotel data: {str(e)}")
            return 0
    
    def collect_revenue_data(self, start_date=None, end_date=None):
        """Collect revenue data"""
        try:
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
            
            # Generate simulated revenue data
            revenue_data = self._generate_simulated_revenue(start_date, end_date)
            
            # Save to database
            for revenue in revenue_data:
                self._save_revenue(revenue)
            
            logger.info(f"Collected {len(revenue_data)} revenue records")
            return len(revenue_data)
            
        except Exception as e:
            logger.error(f"Error collecting revenue data: {str(e)}")
            return 0
    
    def collect_weather_data(self):
        """Collect weather data for Sri Lanka"""
        try:
            if not self.config.OPENWEATHER_API_KEY:
                logger.warning("OpenWeather API key not configured")
                return 0
            
            # Get weather data for major cities in Sri Lanka
            cities = [
                {'name': 'Colombo', 'lat': 6.9271, 'lon': 79.8612},
                {'name': 'Kandy', 'lat': 7.2906, 'lon': 80.6337},
                {'name': 'Galle', 'lat': 6.0535, 'lon': 80.2210},
                {'name': 'Jaffna', 'lat': 9.6615, 'lon': 80.0255},
                {'name': 'Trincomalee', 'lat': 8.5711, 'lon': 81.2335}
            ]
            
            weather_data = []
            for city in cities:
                url = f"http://api.openweathermap.org/data/2.5/weather"
                params = {
                    'lat': city['lat'],
                    'lon': city['lon'],
                    'appid': self.config.OPENWEATHER_API_KEY,
                    'units': 'metric'
                }
                
                response = self.session.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    weather_data.append({
                        'city': city['name'],
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'description': data['weather'][0]['description'],
                        'timestamp': datetime.now()
                    })
            
            # Store weather data in Redis for caching
            from app import redis_client
            redis_client.setex('weather_data', 3600, str(weather_data))  # Cache for 1 hour
            
            logger.info(f"Collected weather data for {len(weather_data)} cities")
            return len(weather_data)
            
        except Exception as e:
            logger.error(f"Error collecting weather data: {str(e)}")
            return 0
    
    def _generate_simulated_arrivals(self, start_date, end_date):
        """Generate simulated tourist arrival data"""
        arrivals = []
        current_date = start_date
        
        # Popular destinations in Sri Lanka
        destinations = [
            'Colombo', 'Kandy', 'Galle', 'Sigiriya', 'Anuradhapura',
            'Polonnaruwa', 'Nuwara Eliya', 'Bentota', 'Mirissa', 'Ella'
        ]
        
        # Top source countries
        source_countries = [
            'India', 'United Kingdom', 'Germany', 'France', 'Australia',
            'United States', 'China', 'Russia', 'Netherlands', 'Canada'
        ]
        
        while current_date <= end_date:
            # Generate 10-50 arrivals per day
            daily_arrivals = random.randint(10, 50)
            
            for _ in range(daily_arrivals):
                arrival = {
                    'date': current_date.date(),
                    'total_arrivals': random.randint(1, 5),
                    'male_count': random.randint(0, 3),
                    'female_count': random.randint(0, 3),
                    'children_count': random.randint(0, 2),
                    'source_country': random.choice(source_countries),
                    'destination': random.choice(destinations),
                    'purpose_of_visit': random.choice(['Leisure', 'Business', 'Education', 'Family']),
                    'duration_of_stay': random.randint(1, 21),
                    'accommodation_type': random.choice(['Hotel', 'Resort', 'Guesthouse', 'Villa'])
                }
                arrivals.append(arrival)
            
            current_date += timedelta(days=1)
        
        return arrivals
    
    def _generate_simulated_hotels(self):
        """Generate simulated hotel data"""
        hotels = []
        
        hotel_data = [
            {'name': 'Cinnamon Grand Colombo', 'category': '5-star', 'type': 'Hotel', 'destination': 'Colombo', 'total_rooms': 500},
            {'name': 'Heritance Kandalama', 'category': '5-star', 'type': 'Resort', 'destination': 'Dambulla', 'total_rooms': 150},
            {'name': 'Galle Face Hotel', 'category': '5-star', 'type': 'Hotel', 'destination': 'Colombo', 'total_rooms': 200},
            {'name': 'Earl\'s Regency Hotel', 'category': '4-star', 'type': 'Hotel', 'destination': 'Kandy', 'total_rooms': 120},
            {'name': 'Fortress Resort & Spa', 'category': '5-star', 'type': 'Resort', 'destination': 'Galle', 'total_rooms': 100},
            {'name': 'Amaya Hills', 'category': '4-star', 'type': 'Resort', 'destination': 'Kandy', 'total_rooms': 80},
            {'name': 'Jetwing Blue', 'category': '4-star', 'type': 'Hotel', 'destination': 'Negombo', 'total_rooms': 160},
            {'name': 'Cinnamon Lodge Habarana', 'category': '4-star', 'type': 'Resort', 'destination': 'Habarana', 'total_rooms': 90},
            {'name': 'Heritance Ahungalla', 'category': '5-star', 'type': 'Resort', 'destination': 'Ahungalla', 'total_rooms': 150},
            {'name': 'Amaya Lake', 'category': '4-star', 'type': 'Resort', 'destination': 'Dambulla', 'total_rooms': 110}
        ]
        
        for hotel_info in hotel_data:
            hotel = {
                'name': hotel_info['name'],
                'category': hotel_info['category'],
                'type': hotel_info['type'],
                'destination': hotel_info['destination'],
                'address': f"Address for {hotel_info['name']}",
                'latitude': random.uniform(6.0, 10.0),
                'longitude': random.uniform(79.0, 82.0),
                'total_rooms': hotel_info['total_rooms'],
                'available_rooms': random.randint(10, hotel_info['total_rooms']),
                'average_price': random.uniform(100, 500),
                'price_range': random.choice(['Budget', 'Mid-range', 'Luxury']),
                'average_rating': random.uniform(3.5, 5.0),
                'total_reviews': random.randint(50, 1000),
                'phone': f"+94 {random.randint(10, 99)} {random.randint(1000000, 9999999)}",
                'email': f"info@{hotel_info['name'].lower().replace(' ', '').replace('&', '')}.com",
                'website': f"www.{hotel_info['name'].lower().replace(' ', '').replace('&', '')}.com"
            }
            hotels.append(hotel)
        
        return hotels
    
    def _generate_simulated_bookings(self):
        """Generate simulated booking data"""
        bookings = []
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now() + timedelta(days=90)
        
        # Generate bookings for the next 3 months
        current_date = start_date
        while current_date <= end_date:
            daily_bookings = random.randint(5, 20)
            
            for _ in range(daily_bookings):
                check_in = current_date + timedelta(days=random.randint(1, 30))
                check_out = check_in + timedelta(days=random.randint(1, 14))
                
                booking = {
                    'hotel_id': random.randint(1, 10),
                    'check_in_date': check_in.date(),
                    'check_out_date': check_out.date(),
                    'booking_date': current_date.date(),
                    'guest_country': random.choice(['India', 'UK', 'Germany', 'France', 'Australia', 'USA']),
                    'guest_type': random.choice(['Individual', 'Family', 'Group', 'Business']),
                    'room_type': random.choice(['Standard', 'Deluxe', 'Suite', 'Family']),
                    'room_count': random.randint(1, 3),
                    'total_amount': random.uniform(100, 2000),
                    'currency': 'USD',
                    'status': random.choice(['confirmed', 'cancelled', 'completed']),
                    'booking_platform': random.choice(['Booking.com', 'Agoda', 'Direct', 'Expedia'])
                }
                bookings.append(booking)
            
            current_date += timedelta(days=1)
        
        return bookings
    
    def _generate_simulated_occupancy(self):
        """Generate simulated occupancy data"""
        occupancy = []
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        current_date = start_date
        while current_date <= end_date:
            for hotel_id in range(1, 11):
                total_rooms = random.randint(80, 500)
                occupied_rooms = random.randint(20, int(total_rooms * 0.9))
                available_rooms = total_rooms - occupied_rooms
                
                occupancy_record = {
                    'hotel_id': hotel_id,
                    'date': current_date.date(),
                    'total_rooms': total_rooms,
                    'occupied_rooms': occupied_rooms,
                    'available_rooms': available_rooms,
                    'occupancy_rate': (occupied_rooms / total_rooms) * 100,
                    'average_daily_rate': random.uniform(100, 500),
                    'revenue_per_available_room': random.uniform(50, 400),
                    'check_ins': random.randint(5, 20),
                    'check_outs': random.randint(5, 20),
                    'cancellations': random.randint(0, 5)
                }
                occupancy.append(occupancy_record)
            
            current_date += timedelta(days=1)
        
        return occupancy
    
    def _generate_simulated_revenue(self, start_date, end_date):
        """Generate simulated revenue data"""
        revenue = []
        current_date = start_date
        
        destinations = ['Colombo', 'Kandy', 'Galle', 'Sigiriya', 'Anuradhapura']
        source_countries = ['India', 'UK', 'Germany', 'France', 'Australia']
        
        while current_date <= end_date:
            daily_revenue = random.randint(1, 5)
            
            for _ in range(daily_revenue):
                total_revenue = random.uniform(10000, 100000)
                
                revenue_record = {
                    'date': current_date.date(),
                    'total_revenue': total_revenue,
                    'accommodation_revenue': total_revenue * random.uniform(0.4, 0.6),
                    'food_beverage_revenue': total_revenue * random.uniform(0.2, 0.3),
                    'transportation_revenue': total_revenue * random.uniform(0.1, 0.2),
                    'entertainment_revenue': total_revenue * random.uniform(0.05, 0.15),
                    'shopping_revenue': total_revenue * random.uniform(0.05, 0.15),
                    'other_revenue': total_revenue * random.uniform(0.02, 0.08),
                    'currency': 'USD',
                    'exchange_rate': random.uniform(300, 350),  # LKR to USD
                    'destination': random.choice(destinations),
                    'source_country': random.choice(source_countries),
                    'average_spending_per_tourist': random.uniform(100, 500),
                    'total_tourists': random.randint(50, 200),
                    'season': random.choice(['Peak', 'Off-peak', 'Shoulder']),
                    'is_holiday_period': random.choice([True, False]),
                    'special_event': random.choice(['', 'New Year', 'Easter', 'Vesak', 'Eid'])
                }
                revenue.append(revenue_record)
            
            current_date += timedelta(days=1)
        
        return revenue
    
    def _save_tourist_arrival(self, arrival_data):
        """Save tourist arrival data to database"""
        try:
            # Get or create source country
            source_country = TouristSource.query.filter_by(name=arrival_data['source_country']).first()
            if not source_country:
                source_country = TouristSource(
                    name=arrival_data['source_country'],
                    code='XX',  # Placeholder
                    region='Unknown'
                )
                db.session.add(source_country)
                db.session.flush()
            
            # Get or create destination
            destination = Destination.query.filter_by(name=arrival_data['destination']).first()
            if not destination:
                destination = Destination(
                    name=arrival_data['destination'],
                    category='Unknown',
                    province='Unknown',
                    district='Unknown'
                )
                db.session.add(destination)
                db.session.flush()
            
            # Create arrival record
            arrival = TouristArrival(
                date=arrival_data['date'],
                total_arrivals=arrival_data['total_arrivals'],
                male_count=arrival_data['male_count'],
                female_count=arrival_data['female_count'],
                children_count=arrival_data['children_count'],
                source_country_id=source_country.id,
                destination_id=destination.id,
                purpose_of_visit=arrival_data['purpose_of_visit'],
                duration_of_stay=arrival_data['duration_of_stay'],
                accommodation_type=arrival_data['accommodation_type']
            )
            
            db.session.add(arrival)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving tourist arrival: {str(e)}")
    
    def _save_hotel(self, hotel_data):
        """Save hotel data to database"""
        try:
            # Get destination
            destination = Destination.query.filter_by(name=hotel_data['destination']).first()
            if not destination:
                destination = Destination(
                    name=hotel_data['destination'],
                    category='Unknown',
                    province='Unknown',
                    district='Unknown'
                )
                db.session.add(destination)
                db.session.flush()
            
            # Check if hotel already exists
            existing_hotel = Hotel.query.filter_by(name=hotel_data['name']).first()
            if existing_hotel:
                return
            
            hotel = Hotel(
                name=hotel_data['name'],
                category=hotel_data['category'],
                type=hotel_data['type'],
                destination_id=destination.id,
                address=hotel_data['address'],
                latitude=hotel_data['latitude'],
                longitude=hotel_data['longitude'],
                total_rooms=hotel_data['total_rooms'],
                available_rooms=hotel_data['available_rooms'],
                average_price=hotel_data['average_price'],
                price_range=hotel_data['price_range'],
                average_rating=hotel_data['average_rating'],
                total_reviews=hotel_data['total_reviews'],
                phone=hotel_data['phone'],
                email=hotel_data['email'],
                website=hotel_data['website']
            )
            
            db.session.add(hotel)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving hotel: {str(e)}")
    
    def _save_booking(self, booking_data):
        """Save booking data to database"""
        try:
            booking = Booking(
                hotel_id=booking_data['hotel_id'],
                check_in_date=booking_data['check_in_date'],
                check_out_date=booking_data['check_out_date'],
                booking_date=booking_data['booking_date'],
                guest_country=booking_data['guest_country'],
                guest_type=booking_data['guest_type'],
                room_type=booking_data['room_type'],
                room_count=booking_data['room_count'],
                total_amount=booking_data['total_amount'],
                currency=booking_data['currency'],
                status=booking_data['status'],
                booking_platform=booking_data['booking_platform']
            )
            
            db.session.add(booking)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving booking: {str(e)}")
    
    def _save_occupancy(self, occupancy_data):
        """Save occupancy data to database"""
        try:
            occupancy = Occupancy(
                hotel_id=occupancy_data['hotel_id'],
                date=occupancy_data['date'],
                total_rooms=occupancy_data['total_rooms'],
                occupied_rooms=occupancy_data['occupied_rooms'],
                available_rooms=occupancy_data['available_rooms'],
                occupancy_rate=occupancy_data['occupancy_rate'],
                average_daily_rate=occupancy_data['average_daily_rate'],
                revenue_per_available_room=occupancy_data['revenue_per_available_room'],
                check_ins=occupancy_data['check_ins'],
                check_outs=occupancy_data['check_outs'],
                cancellations=occupancy_data['cancellations']
            )
            
            db.session.add(occupancy)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving occupancy: {str(e)}")
    
    def _save_revenue(self, revenue_data):
        """Save revenue data to database"""
        try:
            # Get destination and source country
            destination = Destination.query.filter_by(name=revenue_data['destination']).first()
            source_country = TouristSource.query.filter_by(name=revenue_data['source_country']).first()
            
            if not destination or not source_country:
                return
            
            revenue = Revenue(
                date=revenue_data['date'],
                total_revenue=revenue_data['total_revenue'],
                accommodation_revenue=revenue_data['accommodation_revenue'],
                food_beverage_revenue=revenue_data['food_beverage_revenue'],
                transportation_revenue=revenue_data['transportation_revenue'],
                entertainment_revenue=revenue_data['entertainment_revenue'],
                shopping_revenue=revenue_data['shopping_revenue'],
                other_revenue=revenue_data['other_revenue'],
                currency=revenue_data['currency'],
                exchange_rate=revenue_data['exchange_rate'],
                destination_id=destination.id,
                source_country_id=source_country.id,
                average_spending_per_tourist=revenue_data['average_spending_per_tourist'],
                total_tourists=revenue_data['total_tourists'],
                season=revenue_data['season'],
                is_holiday_period=revenue_data['is_holiday_period'],
                special_event=revenue_data['special_event']
            )
            
            revenue.calculate_revenue_usd()
            
            db.session.add(revenue)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving revenue: {str(e)}")