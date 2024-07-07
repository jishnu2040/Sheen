from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Production-specific settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'sheen_db'),
        'USER': os.environ.get('DB_USER', 'sheen_admin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'JISHNU@2040'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files settings
STATIC_ROOT = BASE_DIR / 'staticfiles'
