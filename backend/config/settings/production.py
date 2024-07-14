from .base import *

DEBUG = False

ALLOWED_HOSTS = ['your-production-domain.com']

# Production database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sheen_db',  # Replace with your production database name
        'USER': 'sheen_admin',  # Replace with your production database username
        'PASSWORD': 'JISHNU@2040',  # Replace with your production database password
        'HOST': 'localhost',  # Replace with your production database host or IP
        'PORT': '5432',  # Replace with your production database port
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'

# Email backend settings for production
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your email provider's SMTP server
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sheenweb6@gmail.com'  # Replace with your email address
EMAIL_HOST_PASSWORD = 'egic fotf apkz reqc'  # Replace with your email password or app-specific password
DEFAULT_FROM_EMAIL = 'Celery <sheenonlineservice@gmail.com>'

# Celery configuration for production
CELERY_BROKER_URL = 'redis://localhost:6379/1'  # Use Redis as the broker
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'  # Use Redis as the result backend

# Celery Email configuration
CELERY_EMAIL_TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': True,
}

# Celery Beat schedule (if applicable)
CELERY_BEAT_SCHEDULE = {
    'delete-expired-otps-daily': {
        'task': 'apps.accounts.tasks.delete_expired_otps',  # Update with correct task path
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
}

# Optional: Google API client credentials (if used in production)
GOOGLE_CLIENT_ID = "127240779276-tou36ovq6etmshaji3c9nl80oc7mtkdd.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
SOCIAL_AUTH_PASSWORD = "ZDBDGBB435345"
