"""
Booking Routes
"""
from flask import Blueprint, jsonify, request
from app import db
from app.models import Booking, Package
from app.services import BookingService, PricingService
from app.models.audit import AuditLog

bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')


@bp.route('/quote', methods=['POST'])
def get_price_quote():
    """Get price quote without creating booking"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'package_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Package ID is required'
            }), 400
        
        # Get package
        package = Package.query.get(data['package_id'])
        if not package or not package.is_active:
            return jsonify({
                'success': False,
                'message': 'Package not found or not available'
            }), 404
        
        # Get parameters with defaults
        adults = int(data.get('adults', 2))
        children = int(data.get('children', 0))
        hotel_category = data.get('hotel_category', 'standard')
        airport_pickup = data.get('airport_pickup', False)
        insurance = data.get('insurance', False)
        photographer = data.get('photographer', False)
        
        # Calculate pricing
        pricing = PricingService.calculate_booking_price(
            package=package,
            adults=adults,
            children=children,
            nights=package.duration_nights,
            hotel_category=hotel_category,
            airport_pickup=airport_pickup,
            insurance=insurance,
            photographer=photographer
        )
        
        return jsonify({
            'success': True,
            'pricing': pricing,
            'package': package.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to calculate price',
            'error': str(e)
        }), 500


@bp.route('', methods=['POST'])
def create_booking():
    """Create a new booking"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Create booking using service
        booking = BookingService.create_booking(data)
        
        # Log the action
        AuditLog.log_action(
            action='create_booking',
            user_type='customer',
            user_identifier=data.get('customer', {}).get('email'),
            resource_type='booking',
            resource_id=booking.id,
            description=f'Booking created: {booking.reference}',
            metadata={'package_id': booking.package_id, 'total': booking.total_amount},
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({
            'success': True,
            'message': 'Booking created successfully',
            'booking': booking.to_dict(include_relations=True)
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to create booking',
            'error': str(e)
        }), 500


@bp.route('/<reference>', methods=['GET'])
def get_booking(reference):
    """Get booking by reference"""
    try:
        booking = BookingService.get_booking(reference=reference)
        
        if not booking:
            return jsonify({
                'success': False,
                'message': 'Booking not found'
            }), 404
        
        return jsonify({
            'success': True,
            'booking': booking.to_dict(include_relations=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch booking',
            'error': str(e)
        }), 500


@bp.route('/lookup', methods=['POST'])
def lookup_booking():
    """Look up booking by reference and email (secure guest access)"""
    try:
        data = request.get_json()
        
        if not data or 'reference' not in data or 'email' not in data:
            return jsonify({
                'success': False,
                'message': 'Reference and email are required'
            }), 400
        
        booking = BookingService.lookup_booking(
            reference=data['reference'],
            email=data['email']
        )
        
        if not booking:
            return jsonify({
                'success': False,
                'message': 'Booking not found or email does not match'
            }), 404
        
        return jsonify({
            'success': True,
            'booking': booking.to_dict(include_relations=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to look up booking',
            'error': str(e)
        }), 500


@bp.route('/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        data = request.get_json() or {}
        
        booking = Booking.query.get(booking_id)
        
        if not booking:
            return jsonify({
                'success': False,
                'message': 'Booking not found'
            }), 404
        
        # Verify email for authorization
        if 'email' in data and booking.customer.email.lower() != data['email'].lower():
            return jsonify({
                'success': False,
                'message': 'Unauthorized'
            }), 403
        
        # Cancel booking
        booking = BookingService.cancel_booking(
            booking=booking,
            reason=data.get('reason')
        )
        
        # Log the action
        AuditLog.log_action(
            action='cancel_booking',
            user_type='customer',
            user_identifier=booking.customer.email,
            resource_type='booking',
            resource_id=booking.id,
            description=f'Booking cancelled: {booking.reference}',
            metadata={'refund_amount': booking.refund_amount},
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'success': True,
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict(include_relations=True)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to cancel booking',
            'error': str(e)
        }), 500
