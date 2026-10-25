"""
Destination Routes
"""
from flask import Blueprint, jsonify, request
from app.models import Destination

bp = Blueprint('destinations', __name__, url_prefix='/api/destinations')


@bp.route('', methods=['GET'])
def list_destinations():
    """Get all active destinations"""
    try:
        # Get query parameters
        category = request.args.get('category')
        search = request.args.get('search', '').lower()
        
        # Base query
        query = Destination.query.filter_by(is_active=True)
        
        # Apply filters
        if category and category != 'all':
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(
                db.or_(
                    Destination.name.ilike(f'%{search}%'),
                    Destination.description.ilike(f'%{search}%')
                )
            )
        
        # Execute query
        destinations = query.order_by(Destination.name).all()
        
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


@bp.route('/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    """Get destination by ID"""
    try:
        destination = Destination.query.get(destination_id)
        
        if not destination:
            return jsonify({
                'success': False,
                'message': 'Destination not found'
            }), 404
        
        if not destination.is_active:
            return jsonify({
                'success': False,
                'message': 'Destination not available'
            }), 404
        
        # Include related packages
        include_packages = request.args.get('include_packages', 'true').lower() == 'true'
        
        return jsonify({
            'success': True,
            'destination': destination.to_dict(include_packages=include_packages)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch destination',
            'error': str(e)
        }), 500


@bp.route('/slug/<slug>', methods=['GET'])
def get_destination_by_slug(slug):
    """Get destination by slug"""
    try:
        destination = Destination.query.filter_by(slug=slug, is_active=True).first()
        
        if not destination:
            return jsonify({
                'success': False,
                'message': 'Destination not found'
            }), 404
        
        include_packages = request.args.get('include_packages', 'true').lower() == 'true'
        
        return jsonify({
            'success': True,
            'destination': destination.to_dict(include_packages=include_packages)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch destination',
            'error': str(e)
        }), 500
