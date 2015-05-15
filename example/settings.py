# -*- coding: utf-8 -*-

import os

import django

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'YOUR_SECRET_KEY'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'geodjango',
        'USER': os.environ['USER'],
    }
}

STATIC_URL = '/static/'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

PROJECT_APPS = [
    'airports',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.gis',

    'cities',
] + PROJECT_APPS

if django.VERSION < (1, 7):
    INSTALLED_APPS += [
        'south',
    ]
        
SITE_ID = 1

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, 'templates'),
]

CITIES_POSTAL_CODES = ['ALL']
CITIES_LOCALES = ['ALL']

CITIES_PLUGINS = [
    'cities.plugin.postal_code_ca.Plugin',  # Canada postal codes need region codes remapped to match geonames
]

SPATIALITE_LIBRARY_PATH='/usr/local/lib/mod_spatialite.dylib'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'log_to_stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            },
        },
    'loggers': {
        'airports': {
            'handlers': ['log_to_stdout'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
