#settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: Different secret key from your other projects
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key-for-dev-only')

# Different allowed hosts
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# Isolated apps - only what this project needs
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'shmoukh_admin',
]

# Database - Use PostgreSQL from Railway
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
    # Log database info
    db_config = DATABASES['default']
    print(f"🔗 Using PostgreSQL database: {db_config.get('NAME')} on {db_config.get('HOST')}:{db_config.get('PORT')}")
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Media files configuration for Railway Volume
MEDIA_URL = '/media/'
MEDIA_ROOT = '/data/media'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Custom admin URL - different from your other projects
ADMIN_URL = 'shmoukh-admin/'

# Add this to your settings.py file, preferably after the STATICFILES_STORAGE setting

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/data/media/django.log',  # Using the media volume for persistence
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/data/media/django_errors.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'INFO',  # Set to DEBUG to see all SQL queries
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'products': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'shmoukh_admin': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Custom authentication logger for failed logins
        'django.auth': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
        'handlers': ['console', 'file', 'error_file'],
        'level': 'WARNING',  # Change from ERROR to WARNING to see 404s
        'propagate': False,
        },
        # Custom logger for static files
        'django.staticfiles': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
        'propagate': False,
        },
    }
}

# Add admin email configuration for error notifications
ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'islam.thwabeh@gmail.com')),
]

# Email Configuration - Fully environment variable based
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'webmaster@localhost')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)  # For error emails

# Email logging configuration
if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    print("✅ Email configuration loaded - SMTP backend enabled")
    # Ensure we're using SMTP backend if credentials are provided
    if EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    print("ℹ️  Using console email backend - emails will print to logs")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shmoukh_herbal.middleware.AuthenticationLoggingMiddleware',  # Add this line
]

