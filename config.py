"""
Configuration settings for the Helpdesk System
"""
import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database configuration - SQLite (primary) with Oracle sync support
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'helpdesk.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    # Oracle configuration for data warehouse sync
    # Oracle connection defaults (can be overridden via environment variables)
    ORACLE_USER = os.environ.get('ORACLE_USER', 'Stamford')
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD', 'stamford123')
    ORACLE_HOST = os.environ.get('ORACLE_HOST', 'localhost')
    ORACLE_PORT = os.environ.get('ORACLE_PORT', '1521')
    ORACLE_SERVICE = os.environ.get('ORACLE_SERVICE', 'xepdb1')
    ORACLE_CONNECTION_NAME = os.environ.get('ORACLE_CONNECTION_NAME', 'Application development database')
    ORACLE_ENABLED = True
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_HTTPONLY = True
    
    # Application settings
    TICKETS_PER_PAGE = 10
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
