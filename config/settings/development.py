# config/settings/development.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Additional development-specific settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'