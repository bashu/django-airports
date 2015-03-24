# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class Airport(models.Model):

    name = models.CharField(_("name"), max_length=100)
    code = models.CharField(_("IATA code"), primary_key=True, max_length=3,
                            validators=[MinLengthValidator(3)])

    location = models.PointField()

    country = models.ForeignKey('cities.Country')
    city = models.ForeignKey('cities.City')

    objects = models.GeoManager()

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.name
