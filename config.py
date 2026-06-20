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
    ORACLE_USER = os.environ.get('ORACLE_USER', 'system')
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD', 'SYSTEM')
    ORACLE_HOST = os.environ.get('ORACLE_HOST', 'localhost')
    ORACLE_PORT = os.environ.get('ORACLE_PORT', '1521')
    ORACLE_SERVICE = os.environ.get('ORACLE_SERVICE', 'xepdb1')
    ORACLE_CONNECTION_NAME = os.environ.get('ORACLE_CONNECTION_NAME', 'Application development database')
    ORACLE_ENABLED = os.environ.get('ORACLE_ENABLED', 'True').lower() in ('1', 'true', 'yes')
    ORACLE_USE_AS_PRIMARY = os.environ.get('ORACLE_USE_AS_PRIMARY', 'True').lower() in ('1', 'true', 'yes')
    ORACLE_DB_URI = os.environ.get('ORACLE_DB_URI', '').strip()
    # Enable Oracle sync by default when available.
    # Set ORACLE_ENABLED=False to disable automatic Oracle sync.
    # Set ORACLE_USE_AS_PRIMARY=False to keep SQLite as the main SQLAlchemy database.
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    # Allow enabling admin registration beyond first-admin bootstrap
    ALLOW_REGISTRATION = False
    
    # Application settings
    TICKETS_PER_PAGE = 10
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

    if ORACLE_ENABLED and ORACLE_USE_AS_PRIMARY:
        if ORACLE_DB_URI:
            SQLALCHEMY_DATABASE_URI = ORACLE_DB_URI
        else:
            SQLALCHEMY_DATABASE_URI = (
                f'oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/'
                f'?service_name={ORACLE_SERVICE}'
            )
    else:
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'

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
