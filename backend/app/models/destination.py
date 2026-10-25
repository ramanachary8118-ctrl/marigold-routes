"""
Destination Model
"""
from app import db
from datetime import datetime


class Destination(db.Model):
    """Destination model for travel locations"""
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # mountains, coast, backwaters, heritage
    region = db.Column(db.String(100))
    main_image = db.Column(db.String(500))
    highlights = db.Column(db.JSON)  # List of highlights
    best_months = db.Column(db.JSON)  # List of best months to visit
    recommended_duration = db.Column(db.Integer)  # In days
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    packages = db.relationship('Package', back_populates='destination', lazy='dynamic')
    
    def to_dict(self, include_packages=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'category': self.category,
            'region': self.region,
            'main_image': self.main_image,
            'highlights': self.highlights or [],
            'best_months': self.best_months or [],
            'recommended_duration': self.recommended_duration,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_packages:
            data['packages'] = [p.to_dict() for p in self.packages.filter_by(is_active=True)]
        
        return data
    
    def __repr__(self):
        return f'<Destination {self.name}>'
