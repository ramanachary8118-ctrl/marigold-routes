"""
Package Routes
"""
from flask import Blueprint, jsonify, request
from app.models import Package
from app import db

bp = Blueprint('packages', __name__, url_prefix='/api/packages')


@bp.route('', methods=['GET'])
def list_packages():
    """Get all active packages"""
    try:
        # Get query parameters
        destination_id = request.args.get('destination_id', type=int)
        search = request.args.get('search', '').lower()
        sort_by = request.args.get('sort_by', 'featured')
        
        # Base query
        query = Package.query.filter_by(is_active=True)
        
        # Apply filters
        if destination_id:
            query = query.filter_by(destination_id=destination_id)
        
        if search:
            query = query.filter(
                db.or_(
                    Package.name.ilike(f'%{search}%'),
                    Package.description.ilike(f'%{search}%')
                )
            )
        
        # Apply sorting
        if sort_by == 'price-low':
            query = query.order_by(Package.base_price.asc())
        elif sort_by == 'price-high':
            query = query.order_by(Package.base_price.desc())
        elif sort_by == 'duration-short':
            query = query.order_by(Package.duration_nights.asc())
        elif sort_by == 'duration-long':
            query = query.order_by(Package.duration_nights.desc())
        else:  # featured
            query = query.order_by(Package.is_featured.desc(), Package.display_order.asc(), Package.name.asc())
        
        # Execute query
        packages = query.all()
        
        return jsonify({
            'success': True,
            'count': len(packages),
            'packages': [p.to_dict() for p in packages]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch packages',
            'error': str(e)
        }), 500


@bp.route('/<int:package_id>', methods=['GET'])
def get_package(package_id):
    """Get package by ID with full details"""
    try:
        package = Package.query.get(package_id)
        
        if not package:
            return jsonify({
                'success': False,
                'message': 'Package not found'
            }), 404
        
        if not package.is_active:
            return jsonify({
                'success': False,
                'message': 'Package not available'
            }), 404
        
        # Include itinerary
        include_itinerary = request.args.get('include_itinerary', 'true').lower() == 'true'
        
        return jsonify({
            'success': True,
            'package': package.to_dict(include_itinerary=include_itinerary)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch package',
            'error': str(e)
        }), 500


@bp.route('/slug/<slug>', methods=['GET'])
def get_package_by_slug(slug):
    """Get package by slug"""
    try:
        package = Package.query.filter_by(slug=slug, is_active=True).first()
        
        if not package:
            return jsonify({
                'success': False,
                'message': 'Package not found'
            }), 404
        
        include_itinerary = request.args.get('include_itinerary', 'true').lower() == 'true'
        
        return jsonify({
            'success': True,
            'package': package.to_dict(include_itinerary=include_itinerary)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch package',
            'error': str(e)
        }), 500


@bp.route('/<int:package_id>/related', methods=['GET'])
def get_related_packages(package_id):
    """Get related packages (same destination)"""
    try:
        package = Package.query.get(package_id)
        
        if not package:
            return jsonify({
                'success': False,
                'message': 'Package not found'
            }), 404
        
        # Get other packages for same destination
        related = Package.query.filter(
            Package.destination_id == package.destination_id,
            Package.id != package_id,
            Package.is_active == True
        ).order_by(Package.is_featured.desc(), Package.base_price.asc()).limit(3).all()
        
        return jsonify({
            'success': True,
            'count': len(related),
            'packages': [p.to_dict() for p in related]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch related packages',
            'error': str(e)
        }), 500
