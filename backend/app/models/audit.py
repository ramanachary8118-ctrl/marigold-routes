"""
Audit Log Model
"""
from app import db
from datetime import datetime


class AuditLog(db.Model):
    """Audit log for tracking important actions"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Actor
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    user_type = db.Column(db.String(50))  # admin, customer, system
    user_identifier = db.Column(db.String(200))  # email, username, or ID
    
    # Action details
    action = db.Column(db.String(100), nullable=False)  # login, create_booking, cancel_booking, etc.
    resource_type = db.Column(db.String(100))  # booking, package, destination, etc.
    resource_id = db.Column(db.Integer)
    
    # Details
    description = db.Column(db.Text)
    metadata = db.Column(db.JSON)  # Additional context
    
    # Request info
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(50), default='success')  # success, failure, error
    error_message = db.Column(db.Text)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'user_type': self.user_type,
            'user_identifier': self.user_identifier,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'description': self.description,
            'metadata': self.metadata,
            'ip_address': self.ip_address,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    @staticmethod
    def log_action(action, user_type='system', user_identifier=None, resource_type=None, 
                   resource_id=None, description=None, metadata=None, status='success',
                   error_message=None, ip_address=None, user_agent=None, admin_id=None):
        """Helper method to create audit log entries"""
        log = AuditLog(
            admin_id=admin_id,
            user_type=user_type,
            user_identifier=user_identifier,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            metadata=metadata,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status,
            error_message=error_message
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_identifier}>'
