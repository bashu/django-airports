# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class Airport(models.Model):

    airport_id = models.PositiveIntegerField(primary_key=True)

    name = models.CharField(_("name"), max_length=100)

    iata = models.CharField(_("IATA/FAA code"), blank=True, max_length=3,
                            validators=[MinLengthValidator(3)])
    icao = models.CharField(_("ICAO code"), blank=True, max_length=4,
                            validators=[MinLengthValidator(4)])

    altitude = models.FloatField(_("altitude"), default=0)
    location = models.PointField(_("location"))

    country = models.ForeignKey('cities.Country')
    city = models.ForeignKey('cities.City')

    objects = models.GeoManager()

    class Meta:
        ordering = ['airport_id']

    def __unicode__(self):
        return self.name
