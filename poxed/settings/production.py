from .base import *
import os
import dj_database_url
import environ

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, None),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, None),
    CLOUDINARY_URL=(str, None),
    CLOUDINARY_CLOUD_NAME=(str, None),
    CLOUDINARY_API_KEY=(str, None),
    CLOUDINARY_API_SECRET=(str, None),
    EMAIL_HOST=(str, None),
    EMAIL_PORT=(int, 587),
    EMAIL_HOST_USER=(str, None),
    EMAIL_HOST_PASSWORD=(str, None),
)

# Read .env file from the base directory
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env('DEBUG')
SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS') + ['darcy.phd', 'www.darcy.phd', 'april-wag-2899b9245e95.herokuapp.com', '.herokuapp.com']

# Security settings
SECURE_SSL_REDIRECT = False  # Let Cloudflare handle this
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Let Cloudflare manage HSTS
SECURE_HSTS_PRELOAD = False

# Cloudflare configuration
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cloudflare IPs for proper forwarding
CLOUDFLARE_IPS = [
    '173.245.48.0/20',
    '103.21.244.0/22',
    '103.22.200.0/22',
    '103.31.4.0/22',
    '141.101.64.0/18',
    '108.162.192.0/18',
    '190.93.240.0/20',
    '188.114.96.0/20',
    '197.234.240.0/22',
    '198.41.128.0/17',
    '162.158.0.0/15',
    '104.16.0.0/13',
    '104.24.0.0/14',
    '172.64.0.0/13',
    '131.0.72.0/22',
]

# CSRF and Security Settings
CSRF_TRUSTED_ORIGINS = [
    'https://darcy.phd',
    'https://www.darcy.phd',
    'https://april-wag-2899b9245e95.herokuapp.com',
]

# Ensure consistent URL scheme
PREPEND_WWW = False
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Security and HTTPS settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Let Cloudflare handle this
SECURE_SSL_HOST = None  # Don't force a specific host for SSL

# Update ALLOWED_HOSTS with all variations
ALLOWED_HOSTS = env('ALLOWED_HOSTS') + [
    'darcy.phd',
    'www.darcy.phd',
    'april-wag-2899b9245e95.herokuapp.com',
    '.herokuapp.com',
]

# CSRF settings with proper origins
CSRF_TRUSTED_ORIGINS = [
    'https://darcy.phd',
    'https://www.darcy.phd',
    'https://april-wag-2899b9245e95.herokuapp.com',
]

# Session and cookie settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = None  # Allow the cookie to work on all domains
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = None

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Logging
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
        'level': 'WARNING',
    },
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Additional Cloudflare Headers
MIDDLEWARE.insert(1, 'django.middleware.security.SecurityMiddleware')

# Remove any duplicate MIDDLEWARE entries
MIDDLEWARE = list(dict.fromkeys(MIDDLEWARE))

# Remove any whitenoise references
MIDDLEWARE = [m for m in MIDDLEWARE if 'whitenoise' not in m]

# Consolidated storage settings
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
WAGTAILIMAGES_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Media and Static settings
MEDIA_URL = f'https://res.cloudinary.com/{env("CLOUDINARY_CLOUD_NAME")}/image/upload/'
STATIC_URL = f'https://res.cloudinary.com/{env("CLOUDINARY_CLOUD_NAME")}/static/'

# Cloudinary settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    'MEDIA_TAG': 'media',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
    'STATIC_TAG': 'static',
    'PREFIX': 'wagtail'
}

# Add Cloudinary apps at the beginning of INSTALLED_APPS if not already there
if 'cloudinary_storage' not in INSTALLED_APPS:
    INSTALLED_APPS.insert(0, 'cloudinary_storage')
if 'cloudinary' not in INSTALLED_APPS:
    INSTALLED_APPS.insert(1, 'cloudinary')

# Add Cloudinary apps
INSTALLED_APPS = ['cloudinary_storage', 'cloudinary'] + INSTALLED_APPS

# Cloudinary storage configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
    'SECURE': True,
    'MEDIA_TAG': 'media',
    'STATIC_TAG': 'static',
    'PREFIX': 'wagtail'
}

# Override storage settings for production
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
}

# Update media and static URLs for Cloudinary
MEDIA_URL = f'https://res.cloudinary.com/{env("CLOUDINARY_CLOUD_NAME")}/image/upload/'


# Configure Wagtail to use Cloudinary
WAGTAILIMAGES_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

try:
    from .local import *
except ImportError:
    pass

