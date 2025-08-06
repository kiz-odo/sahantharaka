from app import db
from datetime import datetime
import json

class Hotel(db.Model):
    """Model for hotel/accommodation data"""
    
    __tablename__ = 'hotels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    category = db.Column(db.String(50))  # 5-star, 4-star, 3-star, etc.
    type = db.Column(db.String(50))  # Hotel, Resort, Guesthouse, Villa, etc.
    
    # Location
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    destination = db.relationship('Destination', backref='hotels')
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Capacity and pricing
    total_rooms = db.Column(db.Integer, default=0)
    available_rooms = db.Column(db.Integer, default=0)
    average_price = db.Column(db.Float, default=0.0)
    price_range = db.Column(db.String(50))  # Budget, Mid-range, Luxury
    
    # Ratings and reviews
    average_rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    
    # Amenities and features
    amenities = db.Column(db.Text)  # JSON string of amenities
    facilities = db.Column(db.Text)  # JSON string of facilities
    
    # Contact information
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_amenities(self):
        """Get amenities as list"""
        if self.amenities:
            try:
                return json.loads(self.amenities)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_amenities(self, amenities_list):
        """Set amenities from list"""
        self.amenities = json.dumps(amenities_list)
    
    def get_facilities(self):
        """Get facilities as list"""
        if self.facilities:
            try:
                return json.loads(self.facilities)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_facilities(self, facilities_list):
        """Set facilities from list"""
        self.facilities = json.dumps(facilities_list)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'type': self.type,
            'destination': self.destination.name if self.destination else None,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'total_rooms': self.total_rooms,
            'available_rooms': self.available_rooms,
            'average_price': self.average_price,
            'price_range': self.price_range,
            'average_rating': self.average_rating,
            'total_reviews': self.total_reviews,
            'amenities': self.get_amenities(),
            'facilities': self.get_facilities(),
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Hotel {self.name} ({self.category})>'

class Booking(db.Model):
    """Model for hotel booking data"""
    
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    hotel = db.relationship('Hotel', backref='bookings')
    
    # Booking details
    check_in_date = db.Column(db.Date, nullable=False, index=True)
    check_out_date = db.Column(db.Date, nullable=False, index=True)
    booking_date = db.Column(db.Date, nullable=False, index=True)
    
    # Guest information
    guest_country = db.Column(db.String(100))
    guest_type = db.Column(db.String(50))  # Individual, Family, Group, Business
    
    # Room and pricing
    room_type = db.Column(db.String(50))  # Standard, Deluxe, Suite, etc.
    room_count = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    
    # Booking status
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled, completed
    
    # Platform information
    booking_platform = db.Column(db.String(50))  # Booking.com, Agoda, Direct, etc.
    booking_reference = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'hotel_name': self.hotel.name if self.hotel else None,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None,
            'guest_country': self.guest_country,
            'guest_type': self.guest_type,
            'room_type': self.room_type,
            'room_count': self.room_count,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'status': self.status,
            'booking_platform': self.booking_platform,
            'booking_reference': self.booking_reference,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Booking {self.hotel.name if self.hotel else "Unknown"} - {self.check_in_date} to {self.check_out_date}>'

class Occupancy(db.Model):
    """Model for hotel occupancy data"""
    
    __tablename__ = 'occupancy'
    
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    hotel = db.relationship('Hotel', backref='occupancy_records')
    
    # Date and occupancy data
    date = db.Column(db.Date, nullable=False, index=True)
    total_rooms = db.Column(db.Integer, nullable=False)
    occupied_rooms = db.Column(db.Integer, nullable=False)
    available_rooms = db.Column(db.Integer, nullable=False)
    
    # Occupancy metrics
    occupancy_rate = db.Column(db.Float, nullable=False)  # percentage
    average_daily_rate = db.Column(db.Float, default=0.0)  # ADR
    revenue_per_available_room = db.Column(db.Float, default=0.0)  # RevPAR
    
    # Additional metrics
    check_ins = db.Column(db.Integer, default=0)
    check_outs = db.Column(db.Integer, default=0)
    cancellations = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_occupancy_rate(self):
        """Calculate occupancy rate"""
        if self.total_rooms > 0:
            self.occupancy_rate = (self.occupied_rooms / self.total_rooms) * 100
        else:
            self.occupancy_rate = 0.0
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'hotel_name': self.hotel.name if self.hotel else None,
            'date': self.date.isoformat() if self.date else None,
            'total_rooms': self.total_rooms,
            'occupied_rooms': self.occupied_rooms,
            'available_rooms': self.available_rooms,
            'occupancy_rate': self.occupancy_rate,
            'average_daily_rate': self.average_daily_rate,
            'revenue_per_available_room': self.revenue_per_available_room,
            'check_ins': self.check_ins,
            'check_outs': self.check_outs,
            'cancellations': self.cancellations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Occupancy {self.hotel.name if self.hotel else "Unknown"} - {self.date}: {self.occupancy_rate:.1f}%>'