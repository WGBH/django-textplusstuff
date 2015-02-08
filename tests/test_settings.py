from __future__ import unicode_literals

import os
from django import VERSION as DJANGO_VERSION

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "textplusstuff",
    "tests",
]

if DJANGO_VERSION[0] == 1 and DJANGO_VERSION[1] <= 6:
    INSTALLED_APPS += ("south",)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ROOT_URLCONF = 'tests.urls'
DEBUG = True

TEXTPLUSSTUFF_STUFFGROUPS = {
    'test_group': {
        'name': 'Testing!',
        'description': "For your test models!"
    },
}
SOUTH_TESTS_MIGRATE = True
SKIP_SOUTH_TESTS = True
SOUTH_MIGRATION_MODULES = {
    'textplusstuff': 'ignore',
}
