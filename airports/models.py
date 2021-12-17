from django.contrib.gis.db import models
from django.core.validators import MinLengthValidator
from django.db.models import Manager as GeoManager
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class Airport(models.Model):
    name = models.CharField(_("name"), max_length=100)
    city_name = models.CharField(_("city name"), null=True, blank=True, max_length=100)

    iata = models.CharField(_("IATA/FAA code"), null=True, blank=True, max_length=3, validators=[MinLengthValidator(3)])
    icao = models.CharField(_("ICAO code"), null=True, blank=True, max_length=4, validators=[MinLengthValidator(4)])
    local = models.CharField(_("local code"), null=True, blank=True, max_length=12)
    ident = models.CharField(_("ident code"), null=True, blank=True, max_length=12)

    altitude = models.FloatField(_("altitude"), default=0)
    location = models.PointField(_("location"))

    country = models.ForeignKey("cities.Country", on_delete=models.DO_NOTHING, null=True)
    region = models.ForeignKey("cities.Region", on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey("cities.City", on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=16, default="")

    objects = GeoManager()

    class Meta:  # pylint: disable=C1001
        ordering = ["id"]

    def __str__(self):
        return force_str(self.name)
