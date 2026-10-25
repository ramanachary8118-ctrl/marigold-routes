"""
Contact Enquiry Model
"""
from app import db
from datetime import datetime


class ContactEnquiry(db.Model):
    """Contact form enquiries"""
    __tablename__ = 'contact_enquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Status
    status = db.Column(db.String(50), default='unread')  # unread, read, replied, resolved
    admin_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    replied_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
        }
    
    def __repr__(self):
        return f'<ContactEnquiry {self.name} - {self.subject}>'
