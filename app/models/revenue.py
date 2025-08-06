from app import db
from datetime import datetime
import json

class Revenue(db.Model):
    """Model for tourism revenue data"""
    
    __tablename__ = 'revenue'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    
    # Revenue amounts
    total_revenue = db.Column(db.Float, nullable=False, default=0.0)
    accommodation_revenue = db.Column(db.Float, default=0.0)
    food_beverage_revenue = db.Column(db.Float, default=0.0)
    transportation_revenue = db.Column(db.Float, default=0.0)
    entertainment_revenue = db.Column(db.Float, default=0.0)
    shopping_revenue = db.Column(db.Float, default=0.0)
    other_revenue = db.Column(db.Float, default=0.0)
    
    # Currency and conversion
    currency = db.Column(db.String(3), default='USD')
    exchange_rate = db.Column(db.Float, default=1.0)
    revenue_usd = db.Column(db.Float, default=0.0)  # Revenue in USD
    
    # Geographic breakdown
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    destination = db.relationship('Destination', backref='revenue_records')
    
    # Tourist source breakdown
    source_country_id = db.Column(db.Integer, db.ForeignKey('tourist_sources.id'), nullable=False)
    source_country = db.relationship('TouristSource', backref='revenue_records')
    
    # Metrics
    average_spending_per_tourist = db.Column(db.Float, default=0.0)
    total_tourists = db.Column(db.Integer, default=0)
    
    # Seasonal and trend data
    season = db.Column(db.String(20))  # Peak, Off-peak, Shoulder
    is_holiday_period = db.Column(db.Boolean, default=False)
    special_event = db.Column(db.String(100))  # Any special events affecting revenue
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_total_revenue(self):
        """Calculate total revenue from all sources"""
        self.total_revenue = (
            self.accommodation_revenue +
            self.food_beverage_revenue +
            self.transportation_revenue +
            self.entertainment_revenue +
            self.shopping_revenue +
            self.other_revenue
        )
    
    def calculate_revenue_usd(self):
        """Calculate revenue in USD"""
        self.revenue_usd = self.total_revenue * self.exchange_rate
    
    def calculate_average_spending(self):
        """Calculate average spending per tourist"""
        if self.total_tourists > 0:
            self.average_spending_per_tourist = self.total_revenue / self.total_tourists
        else:
            self.average_spending_per_tourist = 0.0
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'total_revenue': self.total_revenue,
            'accommodation_revenue': self.accommodation_revenue,
            'food_beverage_revenue': self.food_beverage_revenue,
            'transportation_revenue': self.transportation_revenue,
            'entertainment_revenue': self.entertainment_revenue,
            'shopping_revenue': self.shopping_revenue,
            'other_revenue': self.other_revenue,
            'currency': self.currency,
            'exchange_rate': self.exchange_rate,
            'revenue_usd': self.revenue_usd,
            'destination': self.destination.name if self.destination else None,
            'source_country': self.source_country.name if self.source_country else None,
            'average_spending_per_tourist': self.average_spending_per_tourist,
            'total_tourists': self.total_tourists,
            'season': self.season,
            'is_holiday_period': self.is_holiday_period,
            'special_event': self.special_event,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Revenue {self.date}: {self.total_revenue} {self.currency} from {self.source_country.name if self.source_country else "Unknown"}>'

class RevenueSource(db.Model):
    """Model for detailed revenue source breakdown"""
    
    __tablename__ = 'revenue_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    revenue_id = db.Column(db.Integer, db.ForeignKey('revenue.id'), nullable=False)
    revenue = db.relationship('Revenue', backref='source_breakdowns')
    
    # Source details
    source_name = db.Column(db.String(100), nullable=False)
    source_category = db.Column(db.String(50), nullable=False)  # Hotel, Restaurant, Transport, etc.
    source_type = db.Column(db.String(50))  # 5-star, Budget, Local, International, etc.
    
    # Revenue amounts
    amount = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(3), default='USD')
    exchange_rate = db.Column(db.Float, default=1.0)
    amount_usd = db.Column(db.Float, default=0.0)
    
    # Transaction details
    transaction_count = db.Column(db.Integer, default=0)
    average_transaction_value = db.Column(db.Float, default=0.0)
    
    # Geographic and temporal details
    location = db.Column(db.String(200))
    region = db.Column(db.String(100))
    time_period = db.Column(db.String(20))  # Morning, Afternoon, Evening, Night
    
    # Customer demographics
    customer_type = db.Column(db.String(50))  # Domestic, International, Business, Leisure
    customer_segment = db.Column(db.String(50))  # Budget, Mid-range, Luxury
    
    # Performance metrics
    growth_rate = db.Column(db.Float, default=0.0)  # Percentage growth from previous period
    market_share = db.Column(db.Float, default=0.0)  # Percentage of total market
    
    # Additional metadata
    notes = db.Column(db.Text)
    tags = db.Column(db.Text)  # JSON string of tags
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_tags(self):
        """Get tags as list"""
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_tags(self, tags_list):
        """Set tags from list"""
        self.tags = json.dumps(tags_list)
    
    def calculate_amount_usd(self):
        """Calculate amount in USD"""
        self.amount_usd = self.amount * self.exchange_rate
    
    def calculate_average_transaction(self):
        """Calculate average transaction value"""
        if self.transaction_count > 0:
            self.average_transaction_value = self.amount / self.transaction_count
        else:
            self.average_transaction_value = 0.0
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'revenue_id': self.revenue_id,
            'source_name': self.source_name,
            'source_category': self.source_category,
            'source_type': self.source_type,
            'amount': self.amount,
            'currency': self.currency,
            'exchange_rate': self.exchange_rate,
            'amount_usd': self.amount_usd,
            'transaction_count': self.transaction_count,
            'average_transaction_value': self.average_transaction_value,
            'location': self.location,
            'region': self.region,
            'time_period': self.time_period,
            'customer_type': self.customer_type,
            'customer_segment': self.customer_segment,
            'growth_rate': self.growth_rate,
            'market_share': self.market_share,
            'notes': self.notes,
            'tags': self.get_tags(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<RevenueSource {self.source_name} ({self.source_category}): {self.amount} {self.currency}>'