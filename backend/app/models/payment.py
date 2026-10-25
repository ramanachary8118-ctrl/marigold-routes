"""
Payment Model
"""
from app import db
from datetime import datetime


class Payment(db.Model):
    """Payment model for tracking transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    
    # Razorpay IDs
    razorpay_order_id = db.Column(db.String(100), unique=True, index=True)
    razorpay_payment_id = db.Column(db.String(100), unique=True, index=True)
    razorpay_signature = db.Column(db.String(500))
    
    # Payment details
    amount = db.Column(db.Integer, nullable=False)  # Amount in paise
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(50), default='pending')  # pending, success, failed, refunded
    
    # Payment method
    payment_method = db.Column(db.String(50))  # card, upi, netbanking, etc.
    
    # Webhook tracking
    webhook_received = db.Column(db.Boolean, default=False)
    webhook_data = db.Column(db.JSON)
    
    # Refund tracking
    refund_id = db.Column(db.String(100))
    refund_amount = db.Column(db.Integer)
    refund_status = db.Column(db.String(50))
    refunded_at = db.Column(db.DateTime)
    
    # Error tracking
    error_code = db.Column(db.String(100))
    error_description = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    
    # Relationships
    booking = db.relationship('Booking', back_populates='payments')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'razorpay_order_id': self.razorpay_order_id,
            'razorpay_payment_id': self.razorpay_payment_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'refund_id': self.refund_id,
            'refund_amount': self.refund_amount,
            'refund_status': self.refund_status,
            'error_code': self.error_code,
            'error_description': self.error_description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
        }
    
    def __repr__(self):
        return f'<Payment {self.razorpay_order_id}>'
