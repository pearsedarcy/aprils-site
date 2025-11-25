"""
Build-time settings for Docker image creation.
Uses simpler storage backends to avoid manifest issues during collectstatic.
"""
from .production import *

# Use simpler static files storage during build to avoid WhiteNoise manifest issues
# The production storage will be used at runtime
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Also set the legacy setting for compatibility
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Disable database SSL for build (using SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/build.db',
    }
}
