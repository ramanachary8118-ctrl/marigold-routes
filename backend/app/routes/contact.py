"""
Contact Enquiry Routes
"""
from flask import Blueprint, jsonify, request
from app import db
from app.models import ContactEnquiry
from email_validator import validate_email, EmailNotValidError

bp = Blueprint('contact', __name__, url_prefix='/api/contact')


@bp.route('', methods=['POST'])
def submit_enquiry():
    """Submit contact enquiry"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({
                    'success': False,
                    'message': f'{field.capitalize()} is required'
                }), 400
        
        # Validate email
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            return jsonify({
                'success': False,
                'message': 'Invalid email address'
            }), 400
        
        # Create enquiry
        enquiry = ContactEnquiry(
            name=data['name'].strip(),
            email=data['email'].strip().lower(),
            phone=data.get('phone', '').strip(),
            subject=data['subject'].strip(),
            message=data['message'].strip(),
            status='unread'
        )
        
        db.session.add(enquiry)
        db.session.commit()
        
        # TODO: Send notification email to admin
        # TODO: Send acknowledgment email to customer
        
        return jsonify({
            'success': True,
            'message': 'Your enquiry has been submitted successfully. We will get back to you within 24 hours.',
            'enquiry_id': enquiry.id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to submit enquiry',
            'error': str(e)
        }), 500
