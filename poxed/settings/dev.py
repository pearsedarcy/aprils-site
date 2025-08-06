from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rx0-x-@kwk$ay1n$(p01#ovrtx+h0=60cbj^s+xq_nd8v=(4_k"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "meg-834055808010.herokuapp.com", "*.herokuapp.com"]

# Development-specific installed apps
INSTALLED_APPS = INSTALLED_APPS + [
    "debug_toolbar",
    "django_browser_reload",
    "django_extensions",
]

# Correct middleware order is important
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Tailwind development settings
NPM_BIN_PATH = "C:/Users/user/AppData/Roaming/npm/npm.cmd"
INTERNAL_IPS = [
    "127.0.0.1",
]

# Debug toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

# Wagtail settings for development
WAGTAIL_ENABLE_UPDATE_CHECK = True
WAGTAIL_ENABLE_WHATS_NEW_BANNER = True

try:
    from .local import *
except ImportError:
    pass

# --- Production-only settings ---
import dj_database_url
import environ
env = environ.Env(
    DATABASE_URL=(str, None),
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 30
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
