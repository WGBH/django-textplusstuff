from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from django.contrib import admin

from textplusstuff.registry import stuff_registry, findstuff
admin.autodiscover()
findstuff()

urlpatterns = patterns(
    '',
    url(r'^textplusstuff/', include(stuff_registry.urls)),
    url(r'^admin/', include(admin.site.urls))
)
