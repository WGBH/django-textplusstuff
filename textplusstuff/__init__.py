from __future__ import unicode_literals
import sys

import importlib

from textplusstuff.registry import stuff_registry

from django.utils.module_loading import autodiscover_modules
from django.urls import clear_url_caches
from django.conf import settings


default_app_config = 'textplusstuff.apps.TextPlusStuffAppConfig'


__all__ = [
    'autodiscover',
]


def autodiscover(urlconf=None):
    autodiscover_modules('stuff', register_to=stuff_registry)
    # How does Django Admin do this? Magic, apparently.
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        importlib.reload(sys.modules[urlconf])
        clear_url_caches()
