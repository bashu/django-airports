# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Airport


class AirportAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "city", "country")
    search_fields = ("name", "code")
    list_filter = ("country", )
    raw_id_fields = ['city']

admin.site.register(Airport, AirportAdmin)
