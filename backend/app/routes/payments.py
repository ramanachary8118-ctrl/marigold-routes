"""
Payment Routes - Razorpay Integration
"""
from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models import Payment, Booking
from app.models.audit import AuditLog
import razorpay
import hmac
import hashlib

bp = Blueprint('payments', __name__, url_prefix='/api/payments')


def get_razorpay_client():
    """Get Razorpay client"""
    key_id = current_app.config.get('RAZORPAY_KEY_ID')
    key_secret = current_app.config.get('RAZORPAY_KEY_SECRET')
    
    if not key_id or not key_secret:
        raise ValueError("Razorpay credentials not configured")
    
    return razorpay.Client(auth=(key_id, key_secret))


@bp.route('/create-order', methods=['POST'])
def create_payment_order():
    """Create Razorpay payment order"""
    try:
        data = request.get_json()
        
        if not data or 'booking_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Booking ID is required'
            }), 400
        
        # Get booking
        booking = Booking.query.get(data['booking_id'])
        
        if not booking:
            return jsonify({
                'success': False,
                'message': 'Booking not found'
            }), 404
        
        if booking.payment_status == 'success':
            return jsonify({
                'success': False,
                'message': 'Booking already paid'
            }), 400
        
        # Create Razorpay order
        client = get_razorpay_client()
        
        order_data = {
            'amount': booking.total_amount * 100,  # Amount in paise
            'currency': booking.currency,
            'receipt': f'booking_{booking.reference}',
            'notes': {
                'booking_reference': booking.reference,
                'customer_email': booking.customer.email
            }
        }
        
        razorpay_order = client.order.create(data=order_data)
        
        # Create payment record
        payment = Payment(
            booking_id=booking.id,
            razorpay_order_id=razorpay_order['id'],
            amount=booking.total_amount,
            currency=booking.currency,
            status='pending'
        )
        
        db.session.add(payment)
        db.session.commit()
        
        # Log action
        AuditLog.log_action(
            action='create_payment_order',
            user_type='customer',
            user_identifier=booking.customer.email,
            resource_type='payment',
            resource_id=payment.id,
            metadata={'order_id': razorpay_order['id'], 'amount': booking.total_amount}
        )
        
        return jsonify({
            'success': True,
            'order_id': razorpay_order['id'],
            'amount': booking.total_amount,
            'currency': booking.currency,
            'key_id': current_app.config.get('RAZORPAY_KEY_ID'),
            'booking_reference': booking.reference
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f'Payment order creation error: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Failed to create payment order',
            'error': str(e)
        }), 500


@bp.route('/verify', methods=['POST'])
def verify_payment():
    """Verify payment signature"""
    try:
        data = request.get_json()
        
        required_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required payment details'
            }), 400
        
        # Verify signature
        client = get_razorpay_client()
        
        params = {
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        }
        
        # Signature verification
        try:
            client.utility.verify_payment_signature(params)
        except razorpay.errors.SignatureVerificationError:
            return jsonify({
                'success': False,
                'message': 'Invalid payment signature'
            }), 400
        
        # Update payment record
        payment = Payment.query.filter_by(razorpay_order_id=data['razorpay_order_id']).first()
        
        if not payment:
            return jsonify({
                'success': False,
                'message': 'Payment record not found'
            }), 404
        
        # Update payment status
        from datetime import datetime
        payment.razorpay_payment_id = data['razorpay_payment_id']
        payment.razorpay_signature = data['razorpay_signature']
        payment.status = 'success'
        payment.paid_at = datetime.utcnow()
        
        # Update booking status
        booking = payment.booking
        booking.payment_status = 'success'
        booking.status = 'confirmed'
        
        db.session.commit()
        
        # Log action
        AuditLog.log_action(
            action='payment_verified',
            user_type='customer',
            user_identifier=booking.customer.email,
            resource_type='payment',
            resource_id=payment.id,
            metadata={'payment_id': data['razorpay_payment_id']}
        )
        
        # TODO: Send confirmation email here
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'booking_reference': booking.reference
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Payment verification error: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Failed to verify payment',
            'error': str(e)
        }), 500


@bp.route('/webhook', methods=['POST'])
def payment_webhook():
    """Handle Razorpay webhooks"""
    try:
        webhook_secret = current_app.config.get('RAZORPAY_WEBHOOK_SECRET')
        
        if not webhook_secret:
            current_app.logger.warning('Webhook secret not configured')
            return jsonify({'status': 'ok'}), 200
        
        # Verify webhook signature
        signature = request.headers.get('X-Razorpay-Signature')
        
        if not signature:
            return jsonify({'error': 'Missing signature'}), 400
        
        # Verify signature
        body = request.get_data(as_text=True)
        expected_signature = hmac.new(
            webhook_secret.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            current_app.logger.warning('Invalid webhook signature')
            return jsonify({'error': 'Invalid signature'}), 400
        
        # Process webhook event
        event = request.get_json()
        event_type = event.get('event')
        payload = event.get('payload', {}).get('payment', {}).get('entity', {})
        
        current_app.logger.info(f'Webhook received: {event_type}')
        
        # Handle different event types
        if event_type == 'payment.captured':
            order_id = payload.get('order_id')
            payment_id = payload.get('id')
            
            payment = Payment.query.filter_by(razorpay_order_id=order_id).first()
            
            if payment and not payment.webhook_received:
                payment.webhook_received = True
                payment.webhook_data = event
                payment.razorpay_payment_id = payment_id
                payment.status = 'success'
                payment.payment_method = payload.get('method')
                
                booking = payment.booking
                booking.payment_status = 'success'
                booking.status = 'confirmed'
                
                db.session.commit()
                
                # TODO: Send confirmation email
        
        elif event_type == 'payment.failed':
            order_id = payload.get('order_id')
            
            payment = Payment.query.filter_by(razorpay_order_id=order_id).first()
            
            if payment:
                payment.status = 'failed'
                payment.error_code = payload.get('error_code')
                payment.error_description = payload.get('error_description')
                payment.webhook_received = True
                payment.webhook_data = event
                
                booking = payment.booking
                booking.payment_status = 'failed'
                
                db.session.commit()
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        current_app.logger.error(f'Webhook processing error: {str(e)}')
        return jsonify({'error': 'Webhook processing failed'}), 500
