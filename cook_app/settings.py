"""
Django settings for cook_app project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.cookdukan.com','128.199.20.89', 'www.cookdukan.com', '127.0.0.1']


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
    'passlib',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv("DB_PROD_NAME"),
            'USER': os.getenv("DB_PROD_USER"),
            'PASSWORD': os.getenv("DB_PROD_PASSWORD"),
            'HOST': os.getenv("DB_PROD_HOST"),
            'PORT': '3306',
        }
    }


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

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': "[%(asctime)s] %(levelname)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)s] %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#         'json': {
#             'format': '{"@timestamp":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","filename":"%(filename)s",'
#                       '"funcName":"%(funcName)s","line":"%(lineno)s","message":"%(message)s"}'
#         }
#     },
#     'handlers': {
#         # 'console': {
#         #     'level': 'DEBUG',
#         #     'class': 'logging.FileHandler',
#         #     'filename': '/var/log/cook_dukan_log/cash-console.log',
#         #     'formatter': 'simple' if DEBUG else 'json'
#         # },
#         'dashboard': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/var/log/cook_dukan_log/cook-dashboard.log',
#         },
#     },
#     # 'loggers': {
#     #     'dashboard': {
#     #         'handlers': ['dashboard'],
#     #         'level': 'DEBUG',
#     #     },
#     #     'django': {
#     #         'handlers': [ 'dashboard'],
#     #         'level': 'ERROR',
#     #         # 'propagate': True,
#     #     },
#     # },
# }


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'dashboard/static/')
# APPEND_SLASH=False

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


PAGE_SIZE = 6

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
