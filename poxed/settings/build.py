"""
Build-time settings for Docker image creation.
Uses a dummy database but the same static files storage as production
to ensure the manifest is generated correctly.
"""
from .base import *
import os

DEBUG = False
SECRET_KEY = 'build-secret-key-not-for-production'

ALLOWED_HOSTS = ['*']

# Use the same static files storage as production (WhiteNoise with manifest)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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
