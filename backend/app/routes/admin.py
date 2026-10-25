"""
Admin Routes
"""
from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models import Admin, Booking, ContactEnquiry, Destination, Package
from app.models.audit import AuditLog
from functools import wraps
import jwt
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__, url_prefix='/api/admin')


def generate_token(admin_id):
    """Generate JWT token"""
    payload = {
        'admin_id': admin_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )
    
    return token


def token_required(f):
    """Decorator to protect admin routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            
            admin = Admin.query.get(payload['admin_id'])
            
            if not admin or not admin.is_active:
                return jsonify({'success': False, 'message': 'Invalid token'}), 401
            
            request.admin = admin
            
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


@bp.route('/login', methods=['POST'])
def login():
    """Admin login"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        admin = Admin.query.filter_by(username=data['username']).first()
        
        if not admin or not admin.check_password(data['password']):
            # Log failed login attempt
            AuditLog.log_action(
                action='admin_login_failed',
                user_type='admin',
                user_identifier=data['username'],
                status='failure',
                ip_address=request.remote_addr
            )
            
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
        
        if not admin.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is disabled'
            }), 403
        
        # Generate token
        token = generate_token(admin.id)
        
        # Record login
        admin.record_login()
        
        # Log successful login
        AuditLog.log_action(
            action='admin_login_success',
            user_type='admin',
            user_identifier=admin.username,
            admin_id=admin.id,
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'admin': admin.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500


@bp.route('/dashboard', methods=['GET'])
@token_required
def dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get booking stats
        total_bookings = Booking.query.count()
        pending_bookings = Booking.query.filter_by(status='pending').count()
        confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
        cancelled_bookings = Booking.query.filter_by(status='cancelled').count()
        
        # Get revenue (only confirmed bookings with successful payments)
        total_revenue = db.session.query(db.func.sum(Booking.total_amount)).filter(
            Booking.payment_status == 'success'
        ).scalar() or 0
        
        # Get recent bookings
        recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
        
        # Get upcoming departures
        from datetime import date
        upcoming = Booking.query.filter(
            Booking.start_date >= date.today(),
            Booking.status.in_(['pending', 'confirmed'])
        ).order_by(Booking.start_date.asc()).limit(5).all()
        
        # Get enquiry stats
        unread_enquiries = ContactEnquiry.query.filter_by(status='unread').count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_bookings': total_bookings,
                'pending_bookings': pending_bookings,
                'confirmed_bookings': confirmed_bookings,
                'cancelled_bookings': cancelled_bookings,
                'total_revenue': total_revenue,
                'unread_enquiries': unread_enquiries
            },
            'recent_bookings': [b.to_dict(include_relations=True) for b in recent_bookings],
            'upcoming_departures': [b.to_dict(include_relations=True) for b in upcoming]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch dashboard data',
            'error': str(e)
        }), 500


@bp.route('/bookings', methods=['GET'])
@token_required
def list_bookings():
    """List all bookings with filters"""
    try:
        # Get query parameters
        status = request.args.get('status')
        search = request.args.get('search', '').lower()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Base query
        query = Booking.query
        
        # Apply filters
        if status and status != 'all':
            query = query.filter_by(status=status)
        
        if search:
            query = query.join(Booking.customer).filter(
                db.or_(
                    Booking.reference.ilike(f'%{search}%'),
                    db.Customer.full_name.ilike(f'%{search}%'),
                    db.Customer.email.ilike(f'%{search}%')
                )
            )
        
        # Paginate
        paginated = query.order_by(Booking.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'bookings': [b.to_dict(include_relations=True) for b in paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch bookings',
            'error': str(e)
        }), 500


@bp.route('/enquiries', methods=['GET'])
@token_required
def list_enquiries():
    """List contact enquiries"""
    try:
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = ContactEnquiry.query
        
        if status and status != 'all':
            query = query.filter_by(status=status)
        
        paginated = query.order_by(ContactEnquiry.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'enquiries': [e.to_dict() for e in paginated.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch enquiries',
            'error': str(e)
        }), 500


@bp.route('/destinations', methods=['GET'])
@token_required
def list_all_destinations():
    """List all destinations (including inactive)"""
    try:
        destinations = Destination.query.order_by(Destination.name).all()
        
        return jsonify({
            'success': True,
            'count': len(destinations),
            'destinations': [d.to_dict() for d in destinations]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch destinations',
            'error': str(e)
        }), 500


@bp.route('/packages', methods=['GET'])
@token_required
def list_all_packages():
    """List all packages (including inactive)"""
    try:
        packages = Package.query.order_by(Package.name).all()
        
        return jsonify({
            'success': True,
            'count': len(packages),
            'packages': [p.to_dict(include_itinerary=True) for p in packages]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch packages',
            'error': str(e)
        }), 500
