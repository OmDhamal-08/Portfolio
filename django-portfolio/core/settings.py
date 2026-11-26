from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / '.env', encoding='utf-8-sig')
load_dotenv(BASE_DIR / '.env', encoding='utf-8-sig', override=True)


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {'1', 'true', 'yes', 'on'}


DEBUG = env_bool('DEBUG', False)

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-development-only-change-me'
    else:
        raise ImproperlyConfigured(
            'SECRET_KEY must be set when DEBUG=False. Add SECRET_KEY in Vercel Environment Variables.'
        )

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.vercel.app',
]

CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

ENV_ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
if ENV_ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(host.strip() for host in ENV_ALLOWED_HOSTS.split(',') if host.strip())

# No database: portfolio content lives in content/*.json and contact messages
# are delivered by email, so admin, auth and sessions are not needed.
INSTALLED_APPS = [
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portfolio_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'portfolio_app.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {}

# Flash messages ("Message sent") are kept in a signed cookie, not a session.
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'webmaster@localhost')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'dhamalomm@gmail.com')

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', True)
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    CSRF_TRUSTED_ORIGINS = [
        'https://*.vercel.app',
    ]
    if CUSTOM_DOMAIN:
        CSRF_TRUSTED_ORIGINS.append(f'https://{CUSTOM_DOMAIN}')

# Vercel serves Django through a serverless function; WhiteNoise lets this app
# serve its static portfolio assets without adding a separate storage service.
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}
WHITENOISE_USE_FINDERS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

if os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL'),
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# How long parsed content/*.json files stay cached (seconds). The cache key
# includes each file's modification time, so edits show up immediately.
CONTENT_CACHE_TIMEOUT = int(os.environ.get("CONTENT_CACHE_TIMEOUT", 60 * 60))
