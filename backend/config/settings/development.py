from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Development-specific settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sheen_db',
        'USER': 'sheen_admin',
        'PASSWORD': 'JISHNU@2040',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
