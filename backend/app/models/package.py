"""
Package Models
"""
from app import db
from datetime import datetime


class Package(db.Model):
    """Travel package model"""
    __tablename__ = 'packages'
    
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    duration_nights = db.Column(db.Integer, nullable=False)
    base_price = db.Column(db.Integer, nullable=False)  # Price in rupees (paise for calculations)
    currency = db.Column(db.String(10), default='INR')
    
    # Inclusions and Exclusions
    inclusions = db.Column(db.JSON)  # List of included services
    exclusions = db.Column(db.JSON)  # List of excluded services
    
    # Accommodation
    accommodation_type = db.Column(db.String(100))  # e.g., "3-star hotels"
    hotel_upgrade_superior = db.Column(db.Integer, default=900)  # Per night
    hotel_upgrade_luxury = db.Column(db.Integer, default=2400)  # Per night
    
    # Additional info
    highlights = db.Column(db.JSON)
    main_image = db.Column(db.String(500))
    gallery_images = db.Column(db.JSON)  # List of image URLs
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    destination = db.relationship('Destination', back_populates='packages')
    itinerary_days = db.relationship('PackageItinerary', back_populates='package', 
                                     order_by='PackageItinerary.day_number',
                                     cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='package', lazy='dynamic')
    
    def to_dict(self, include_itinerary=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'destination_id': self.destination_id,
            'destination_name': self.destination.name if self.destination else None,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'duration_days': self.duration_days,
            'duration_nights': self.duration_nights,
            'base_price': self.base_price,
            'currency': self.currency,
            'inclusions': self.inclusions or [],
            'exclusions': self.exclusions or [],
            'accommodation_type': self.accommodation_type,
            'hotel_upgrade_superior': self.hotel_upgrade_superior,
            'hotel_upgrade_luxury': self.hotel_upgrade_luxury,
            'highlights': self.highlights or [],
            'main_image': self.main_image,
            'gallery_images': self.gallery_images or [],
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_itinerary:
            data['itinerary'] = [day.to_dict() for day in self.itinerary_days]
        
        return data
    
    def __repr__(self):
        return f'<Package {self.name}>'


class PackageItinerary(db.Model):
    """Day-by-day itinerary for packages"""
    __tablename__ = 'package_itineraries'
    
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    activities = db.Column(db.JSON)  # List of activities
    meals = db.Column(db.JSON)  # e.g., ["breakfast", "dinner"]
    accommodation = db.Column(db.String(200))
    
    # Relationships
    package = db.relationship('Package', back_populates='itinerary_days')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'day_number': self.day_number,
            'title': self.title,
            'description': self.description,
            'activities': self.activities or [],
            'meals': self.meals or [],
            'accommodation': self.accommodation,
        }
    
    def __repr__(self):
        return f'<PackageItinerary Day {self.day_number} - {self.package.name}>'
