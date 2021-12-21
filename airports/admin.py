from django.contrib import admin

from .models import Airport


class AirportAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "iata", "icao", "city", "region", "country")
    search_fields = ("name", "iata", "icao")
    list_filter = ("country",)
    raw_id_fields = ["city", "region", "country"]


admin.site.register(Airport, AirportAdmin)
