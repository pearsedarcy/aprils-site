"""
Build-time settings for Docker image creation.
Uses simple static files storage that doesn't validate CSS references.
"""
from .base import *
import os

DEBUG = False
SECRET_KEY = 'build-secret-key-not-for-production'

ALLOWED_HOSTS = ['*']

# Use simple static files storage during build - no manifest validation
# This avoids the "calendar-icons.svg not found" error from Django admin CSS
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
    os.path.join(BASE_DIR, "theme/static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = "/static/"

# Dummy database for build (just needs to not error on collectstatic)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/build.db',
    }
}

# Dummy Cloudinary settings for build
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dummy',
    'API_KEY': 'dummy',
    'API_SECRET': 'dummy',
}

# Use filesystem for media during build
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
