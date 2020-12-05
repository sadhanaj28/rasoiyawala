"""
Django settings for cook_app project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.data_types['DateTimeField'] = 'datetime'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@3#le)2xi@+zl+2#lb)*0iq=sh*r18n1wz*p=!zb^+o=q^tj71'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'cookwalabook.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cook_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cook_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_97b608cb8a2bdb0',
        'USER': 'b426b54596dad4',
        'PASSWORD': 'f3951f14',
        'HOST': 'us-cdbr-east-02.cleardb.com',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json': {
            'format': '{"@timestamp":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","filename":"%(filename)s",'
                      '"funcName":"%(funcName)s","line":"%(lineno)s","message":"%(message)s"}'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'cook_app/log_files/console.log',
            'formatter': 'simple' if DEBUG else 'json'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,   
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# APPEND_SLASH=False

# Local
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# local
# COOK_GET_COOK_LIST_API = 'http://127.0.0.1:8000/api/cook/cooks_list/'
# COOK_GET_AREA_LIST = 'http://127.0.0.1:8000/api/cook/area_list/'
# COOK_CREATE_COOK_API = 'http://127.0.0.1:8000/api/cook/cook_details/'
# COOK_UPLOAD_COOK_IMAGE_API = 'http://127.0.0.1:8000/api/cook/cook_image/'

# heroku prod
COOK_GET_COOK_LIST_API = 'http://cookwalabook.herokuapp.com/api/cook/cooks_list/'
COOK_GET_AREA_LIST = 'http://cookwalabook.herokuapp.com/api/cook/area_list/'
COOK_CREATE_COOK_API = 'http://cookwalabook.herokuapp.com/api/cook/cook_details/'
COOK_UPLOAD_COOK_IMAGE_API = 'http://cookwalabook.herokuapp.com/api/cook/cook_image/'

PAGE_SIZE = 6

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
