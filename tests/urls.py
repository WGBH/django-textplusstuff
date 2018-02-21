from __future__ import unicode_literals

from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin

from textplusstuff.registry import stuff_registry

urlpatterns = [
    url(r'^textplusstuff/', include(stuff_registry.urls)),
    path('admin/', admin.site.urls)
]
