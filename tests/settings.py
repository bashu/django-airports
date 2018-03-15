# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "!2*nm%ps%x8!ykyb^s9+!l1vcmeh+(f&de%br=js*7(5i_rmet"

# Travis uses trusty which have no mod_spatialite
if 'TRAVIS' in os.environ:
    SPATIALITE_LIBRARY_PATH = 'mod_spatialite'

DATABASES = {
    "default": {
        "ENGINE": 'django.contrib.gis.db.backends.spatialite',
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    'cities',
    "airports",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
