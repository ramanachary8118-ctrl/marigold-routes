"""
Booking Models
"""
from app import db
from datetime import datetime
import secrets
import string


class Booking(db.Model):
    """Booking model for customer reservations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Relationships
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=False)
    
    # Travel details
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, default=0)
    
    # Hotel category
    hotel_category = db.Column(db.String(50), default='standard')  # standard, superior, luxury
    
    # Special requests
    special_requests = db.Column(db.Text)
    
    # Package snapshot (preserve pricing even if package changes)
    package_snapshot = db.Column(db.JSON, nullable=False)
    
    # Pricing breakdown
    base_price = db.Column(db.Integer, nullable=False)
    travellers_price = db.Column(db.Integer, default=0)
    hotel_upgrade_price = db.Column(db.Integer, default=0)
    extras_price = db.Column(db.Integer, default=0)
    subtotal = db.Column(db.Integer, nullable=False)
    gst = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    
    # Status
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, confirmed, cancelled, completed
    payment_status = db.Column(db.String(50), default='pending')  # pending, success, failed, refunded
    
    # Cancellation
    cancelled_at = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.Text)
    refund_amount = db.Column(db.Integer)
    refund_status = db.Column(db.String(50))  # requested, approved, processed, completed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = db.relationship('Customer', back_populates='bookings')
    package = db.relationship('Package', back_populates='bookings')
    travellers = db.relationship('BookingTraveller', back_populates='booking', 
                                 cascade='all, delete-orphan')
    extras = db.relationship('BookingExtra', back_populates='booking',
                            cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='booking', lazy='dynamic')
    
    @staticmethod
    def generate_reference():
        """Generate unique booking reference"""
        prefix = 'MR'
        # Use timestamp and random string
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return f'{prefix}{timestamp}{random_str}'
    
    def to_dict(self, include_relations=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'reference': self.reference,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'adults': self.adults,
            'children': self.children,
            'hotel_category': self.hotel_category,
            'special_requests': self.special_requests,
            'package_snapshot': self.package_snapshot,
            'pricing': {
                'base_price': self.base_price,
                'travellers_price': self.travellers_price,
                'hotel_upgrade_price': self.hotel_upgrade_price,
                'extras_price': self.extras_price,
                'subtotal': self.subtotal,
                'gst': self.gst,
                'total_amount': self.total_amount,
                'currency': self.currency,
            },
            'status': self.status,
            'payment_status': self.payment_status,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'cancellation_reason': self.cancellation_reason,
            'refund_amount': self.refund_amount,
            'refund_status': self.refund_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_relations:
            data['customer'] = self.customer.to_dict() if self.customer else None
            data['package'] = self.package.to_dict() if self.package else None
            data['travellers'] = [t.to_dict() for t in self.travellers]
            data['extras'] = [e.to_dict() for e in self.extras]
        
        return data
    
    def __repr__(self):
        return f'<Booking {self.reference}>'


class BookingTraveller(db.Model):
    """Traveller details for booking"""
    __tablename__ = 'booking_travellers'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    is_child = db.Column(db.Boolean, default=False)
    
    # Relationships
    booking = db.relationship('Booking', back_populates='travellers')
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'age': self.age,
            'is_child': self.is_child,
        }
    
    def __repr__(self):
        return f'<BookingTraveller {self.full_name}>'


class BookingExtra(db.Model):
    """Additional services for booking"""
    __tablename__ = 'booking_extras'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)  # airport_pickup, insurance, photographer
    service_description = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    # Relationships
    booking = db.relationship('Booking', back_populates='extras')
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
            'service_description': self.service_description,
            'price': self.price,
            'quantity': self.quantity,
        }
    
    def __repr__(self):
        return f'<BookingExtra {self.service_name}>'
