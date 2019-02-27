#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-airports
------------

Tests for `django-airports` models module.
"""
from cities.models import Country, City, Region
from django.contrib.gis.geos import Point
from django.test import TestCase

from airports.models import Airport


class TestAirports(TestCase):
    def setUp(self):
        country = Country.objects.create(population=0)
        region = Region.objects.create(
            name_std='region',
            country=country
        )
        city = City.objects.create(
            name='Goroka',
            name_std='Goroka',
            country=country,
            region=region,
            location=Point(0, 0),
            population=0,
        )

        pnt = Point(-6.081689834590001, 145.391998291, srid=4326)

        self.sut = Airport.objects.create(
            airport_id=1,
            name="Goroka Airport",
            location=pnt,
            city=city,
            iata='XX88',
            icao='XX88',
            altitude=1000,
            country=country,
        )

    def test_not_none(self):
        self.assertIsNotNone(self.sut)
        self.assertIsNotNone(self.sut.airport_id)
        self.assertIsNotNone(self.sut.name)
        self.assertIsNotNone(self.sut.iata)
        self.assertIsNotNone(self.sut.icao)
        self.assertIsNotNone(self.sut.altitude)
        self.assertIsNotNone(self.sut.location)
        self.assertIsNotNone(self.sut.country)
        self.assertIsNotNone(self.sut.city)

    def tearDown(self):
        pass
