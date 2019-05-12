"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
import sys
from .utils.utils import load_json

import django
#django.setup()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
CONFIG_DATA = load_json(BASE_DIR + '/config.json')
SECRET_KEY =  CONFIG_DATA["SECRET_KEY"]
#SECRET_KEY = 'q39d(mu9bf9a2-(%rgvkc7w$r0h=0&8d9f)dd-iu6o^1@=ut#7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:test@localhost:7687')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_neomodel',
    'crispy_forms',
    'polls.apps.PollsConfig',
    'carbon_calculator',
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

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'carbon_calculator.context_processors.static_media',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

CRISPY_TEMPLATE_PACK = 'bootstrap'
# CRISPY_TEMPLATE_PACK = 'uni_form'
CRISPY_FAIL_SILENTLY = not DEBUG

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL')

#from neomodel import config
#config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'  # default


#NEO4J_DATABASES = {
#    'default' : {
#        'HOST':'localhost',
#        'PORT':7474,
#        'ENDPOINT':'/db/data'
#    }
#}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
IMAGE_LOC = STATIC_URL + 'images/'

EVENT_LOGO = IMAGE_LOC+'ACCC Logo Jpg.jpg'
HOST_LOGO = IMAGE_LOC+'EGS Logo Jpg.jpg'
SPONSOR_LOGO = IMAGE_LOC+'HGCF.jpg'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{module} {levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
    #    'special': {
    #        '()': 'project.logging.SpecialFilter',
    #        'foo': 'bar',
    #    },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        #    'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    #    'myproject.custom': {
    #        'handlers': ['console', 'mail_admins'],
    #        'level': 'INFO',
    #        'filters': ['special']
    #    }
    }
}