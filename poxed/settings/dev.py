from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-rx0-x-@kwk$ay1n$(p01#ovrtx+h0=60cbj^s+xq_nd8v=(4_k"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

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
