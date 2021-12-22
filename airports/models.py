from django.contrib.gis.db import models
from django.core.validators import MinLengthValidator
from django.db.models import Manager as GeoManager
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class Airport(models.Model):
    name = models.CharField(_("name"), max_length=100, help_text=_("The official airport name, including \"Airport\", \"Airstrip\", etc."))
    municipality = models.CharField(_("municipality"), null=True, blank=True, max_length=100, help_text=_("The primary municipality that the airport serves (when available). Note that this is not necessarily the municipality where the airport is physically located."))

    iata = models.CharField(_("IATA/FAA code"), null=True, blank=True, max_length=3, validators=[MinLengthValidator(3)], help_text=("The three-letter IATA code for the airport (if it has one)."))
    icao = models.CharField(_("ICAO code"), null=True, blank=True, max_length=4, validators=[MinLengthValidator(4)])
    ident = models.CharField(_("identifier"), null=True, blank=True, max_length=12, help_text=_("The text identifier used in the OurAirports URL"))
    local_code = models.CharField(_("local country code"), null=True, blank=True, max_length=12, help_text=_("The local country code for the airport"))
    type = models.CharField(_("type"), max_length=16, default="", help_text=_("The type of the airport. Allowed values are \"closed_airport\", \"heliport\", \"large_airport\", \"medium_airport\", \"seaplane_base\", and \"small_airport\"."))

    altitude = models.FloatField(_("altitude"), default=0, help_text=_("The airport elevation MSL in feet (not metres)."))
    location = models.PointField(_("coordinates"))

    country = models.ForeignKey("cities.Country", on_delete=models.DO_NOTHING, null=True)
    region = models.ForeignKey("cities.Region", on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey("cities.City", on_delete=models.DO_NOTHING, null=True)

    objects = GeoManager()

    class Meta:  # pylint: disable=C1001
        ordering = ["id"]

    def __str__(self):
        return force_str(self.name)
