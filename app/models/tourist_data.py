from app import db
from datetime import datetime
import json

class TouristArrival(db.Model):
    """Model for tourist arrival data"""
    
    __tablename__ = 'tourist_arrivals'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    total_arrivals = db.Column(db.Integer, nullable=False)
    male_count = db.Column(db.Integer, default=0)
    female_count = db.Column(db.Integer, default=0)
    children_count = db.Column(db.Integer, default=0)
    
    # Source country information
    source_country_id = db.Column(db.Integer, db.ForeignKey('tourist_sources.id'), nullable=False)
    source_country = db.relationship('TouristSource', backref='arrivals')
    
    # Destination information
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    destination = db.relationship('Destination', backref='arrivals')
    
    # Additional metadata
    purpose_of_visit = db.Column(db.String(50))  # Leisure, Business, Education, etc.
    duration_of_stay = db.Column(db.Integer)  # in days
    accommodation_type = db.Column(db.String(50))  # Hotel, Guesthouse, Resort, etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'total_arrivals': self.total_arrivals,
            'male_count': self.male_count,
            'female_count': self.female_count,
            'children_count': self.children_count,
            'source_country': self.source_country.name if self.source_country else None,
            'destination': self.destination.name if self.destination else None,
            'purpose_of_visit': self.purpose_of_visit,
            'duration_of_stay': self.duration_of_stay,
            'accommodation_type': self.accommodation_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<TouristArrival {self.date}: {self.total_arrivals} from {self.source_country.name if self.source_country else "Unknown"}>'

class TouristSource(db.Model):
    """Model for tourist source countries"""
    
    __tablename__ = 'tourist_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    code = db.Column(db.String(3), unique=True)  # ISO country code
    region = db.Column(db.String(50))  # Asia, Europe, Americas, etc.
    
    # Statistics
    total_tourists = db.Column(db.Integer, default=0)
    average_stay_duration = db.Column(db.Float, default=0.0)
    average_spending = db.Column(db.Float, default=0.0)
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'region': self.region,
            'total_tourists': self.total_tourists,
            'average_stay_duration': self.average_stay_duration,
            'average_spending': self.average_spending,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<TouristSource {self.name}>'

class Destination(db.Model):
    """Model for tourist destinations in Sri Lanka"""
    
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    category = db.Column(db.String(50))  # Beach, Cultural, Wildlife, Hill Country, etc.
    province = db.Column(db.String(50))
    district = db.Column(db.String(50))
    
    # Geographic coordinates
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Statistics
    total_visitors = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    popularity_score = db.Column(db.Float, default=0.0)
    
    # Features and amenities
    features = db.Column(db.Text)  # JSON string of features
    activities = db.Column(db.Text)  # JSON string of activities
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_features(self):
        """Get features as list"""
        if self.features:
            try:
                return json.loads(self.features)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_features(self, features_list):
        """Set features from list"""
        self.features = json.dumps(features_list)
    
    def get_activities(self):
        """Get activities as list"""
        if self.activities:
            try:
                return json.loads(self.activities)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_activities(self, activities_list):
        """Set activities from list"""
        self.activities = json.dumps(activities_list)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'province': self.province,
            'district': self.district,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'total_visitors': self.total_visitors,
            'average_rating': self.average_rating,
            'popularity_score': self.popularity_score,
            'features': self.get_features(),
            'activities': self.get_activities(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Destination {self.name} ({self.category})>'