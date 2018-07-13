# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Airport


class AirportAdmin(admin.ModelAdmin):
    list_display = ("airport_id", "name", "iata", "icao", "city", "country")
    search_fields = ("name", "iata", "icao")
    list_filter = ("country", )
    raw_id_fields = ['city']

admin.site.register(Airport, AirportAdmin)
