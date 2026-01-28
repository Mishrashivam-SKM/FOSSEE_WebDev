"""
Production settings for Chemical Equipment Visualizer project.

This configuration is optimized for deployment on Railway with SQLite.
For PostgreSQL, update the DATABASE_URL environment variable.
"""

import os
import dj_database_url
from .base import *

DEBUG = False

# Get secret key from environment (required in production)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Parse allowed hosts from environment
allowed_hosts_str = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]

# Add Railway domain if present
railway_domain = os.environ.get('RAILWAY_STATIC_URL', '')
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain.replace('https://', '').replace('http://', ''))

# Database - SQLite for Railway, or PostgreSQL via DATABASE_URL
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files - using WhiteNoise for serving
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# WhiteNoise configuration
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Only enable HTTPS settings if not in Railway (Railway handles SSL)
if not os.environ.get('RAILWAY_ENVIRONMENT'):
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# CORS settings for production
cors_origins_str = os.environ.get('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',') if origin.strip()]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
