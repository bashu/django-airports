# -*- coding: utf-8 -*-

from django.contrib.gis.db import models

try:
    from django.utils.encoding import force_unicode as force_text
except (NameError, ImportError):
    from django.utils.encoding import force_text
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

from .conf import DJANGO_VERSION

if DJANGO_VERSION < 2:
    from django.contrib.gis.db.models import GeoManager
else:
    from django.db.models import Manager as GeoManager


@python_2_unicode_compatible
class Airport(models.Model):
    airport_id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(_("name"), max_length=100)

    iata = models.CharField(_("IATA/FAA code"),
                            blank=True,
                            max_length=3,
                            validators=[MinLengthValidator(3)],
                            )

    icao = models.CharField(_("ICAO code"),
                            blank=True,
                            max_length=4,
                            validators=[MinLengthValidator(4)]
                            )

    altitude = models.FloatField(_("altitude"), default=0)
    location = models.PointField(_("location"))

    country = models.ForeignKey('cities.Country', on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey('cities.City', on_delete=models.DO_NOTHING, null=True)

    objects = GeoManager()

    class Meta:  # pylint: disable=C1001
        ordering = ['airport_id']

    def __str__(self):
        return force_text(self.name)
