# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import distro

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "!2*nm%ps%x8!ykyb^s9+!l1vcmeh+(f&de%br=js*7(5i_rmet"

# needed since travis uses Ubuntu 14.04
if distro.linux_distribution() == ('Ubuntu', '16.04', 'Xenial Xerus') or \
    distro.linux_distribution() == (u'Linux Mint', u'18.3', u'Sylvia'):
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
