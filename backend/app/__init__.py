"""
Marigold Routes - Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    # Configure CORS
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    CORS(app, resources={
        r"/api/*": {
            "origins": [frontend_url],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    from app.routes import destinations, packages, bookings, payments, contact, admin, health
    
    app.register_blueprint(destinations.bp)
    app.register_blueprint(packages.bp)
    app.register_blueprint(bookings.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(health.bp)
    
    # Error handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'message': 'Bad request', 'error': str(error)}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return {'message': 'Unauthorized access', 'error': str(error)}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'message': 'Forbidden', 'error': str(error)}, 403
    
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Resource not found', 'error': str(error)}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Internal error: {error}')
        return {'message': 'Internal server error'}, 500
