"""
Django settings for dataset_retriever project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from pathlib import Path
import os

# OAUTH related environment variables
OAUTH2_PROVIDER_AUTHORIZATION_URL = os.getenv('OAUTH2_PROVIDER_AUTHORIZATION_URL')
OAUTH2_PROVIDER_TOKEN_URL = os.getenv('OAUTH2_PROVIDER_TOKEN_URL')
OAUTH2_CLIENT_ID = os.getenv('OAUTH2_CLIENT_ID')
OAUTH2_CLIENT_SECRET = os.getenv('OAUTH2_CLIENT_SECRET')
OAUTH2_REDIRECT_URI = os.getenv('OAUTH2_REDIRECT_URI')
OAUTH2_SCOPE = os.getenv('OAUTH2_SCOPE')
# OAUTH2_SCOPE = "datahub:dataexports:download,read datasets:bds:read reporting:dataset:fetch,list reporting:job:create,download,fetch,list"

# Brightspace related environment variables
BDS_API_URL = os.getenv('BDS_API_URL')
# SMB related environment variables
NETWORK_DRIVE_USERNAME = os.getenv('NETWORK_DRIVE_USERNAME')
NETWORK_DRIVE_PASSWORD = os.getenv('NETWORK_DRIVE_PASSWORD')
NETWORK_DRIVE_SERVER = os.getenv('NETWORK_DRIVE_SERVER')
NETWORK_DRIVE_PATH = os.getenv('NETWORK_DRIVE_PATH')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s4&hznh9bz3y7&8&la$hawthpphvsc88au0&f*f_++8m^w0@n3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*', 'dataset-retriever.ltc.bcit.ca', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'oauth2_provider',
    'corsheaders',

    'django_celery_beat',

    'task_functions',
    'oauth_connector'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'dataset_retriever.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dataset_retriever.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        # 'NAME': BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery settings
# CELERY_RESULT_BACKEND = 'cache'
# CELERY_CACHE_BACKEND = 'memory'
# CELERYD_TIME_LIMIT=1800

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            "redis://localhost:6379",
        ],
    }
}

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERYD_TIME_LIMIT=1800

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "custom": {
            "format": "{levelname} {asctime} {name} {funcName} >>> {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "custom",
        },
        "file_log": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "dev.log",
            "formatter": "custom",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "filters": ['require_debug_true']
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "task_functions": {
            "handlers": ["console","file_log"],
            "level": "INFO",
            "propagate": True,
        },
        "oauth_connector": {
            "handlers": ["console","file_log"],
            "level": "INFO",
            "propagate": True,
        },
        "celery.task": {
            "handlers": ["console","file_log"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}
