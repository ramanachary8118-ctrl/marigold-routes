"""
Application Configuration
"""
import os
from datetime import timedelta


class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/marigold_routes')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Razorpay
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
    RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET', '')
    
    # Resend (Email)
    RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'noreply@marigoldroutes.example')
    
    # Application
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')
    
    # Pricing
    GST_RATE = 0.05
    CHILD_DISCOUNT_RATE = 0.30
    
    # Security
    BCRYPT_LOG_ROUNDS = 12
    MAX_LOGIN_ATTEMPTS = 5
    RATE_LIMIT_PER_MINUTE = 60


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Ensure critical env vars are set
    if not os.getenv('SECRET_KEY'):
        raise ValueError("SECRET_KEY must be set in production")
    if not os.getenv('DATABASE_URL'):
        raise ValueError("DATABASE_URL must be set in production")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/marigold_routes_test'
    BCRYPT_LOG_ROUNDS = 4  # Faster for tests
