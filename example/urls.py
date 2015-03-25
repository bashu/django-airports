# -*- coding: utf-8 -*-

from django.conf.urls import patterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
