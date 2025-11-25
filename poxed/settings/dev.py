from .base import *
import shutil

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable with fallback for development only
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-dev-only-change-in-production')

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

# Development database - SQLite for simplicity
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

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

# Email backend for development - prints to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Tailwind development settings - find npm dynamically
NPM_BIN_PATH = shutil.which('npm') or "npm"

INTERNAL_IPS = [
    "127.0.0.1",
]

# Debug toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    'IS_RUNNING_TESTS': False,  # Allow tests to run without debug toolbar errors
}

# Wagtail settings for development
WAGTAIL_ENABLE_UPDATE_CHECK = True
WAGTAIL_ENABLE_WHATS_NEW_BANNER = True

# Use local file storage in development (not Cloudinary)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Disable secure cookies in development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

try:
    from .local import *
except ImportError:
    pass
