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
from airports.management.commands.airports import get_location_info, create_airport

class TestAirports(TestCase):
    def setUp(self):
        self.country = Country(
                slug='United-States',
                name='United States',
                code='US',
                code3='USA',
                population=310232863,
                area=9629091,
                currency='USD',
                currency_name='Dollar',
                currency_symbol='$',
                language_codes='en-US,es-US,haw,fr',
                phone='1',
                tld='us',
                capital='Washington',
            )
        self.country.save()
        self.region = Region(
                slug='California_US.CA',
                name='California',
                name_std='California',
                code='CA',
                country=self.country,
            )
        self.region.save()
        self.city = City(
                slug='5323401-Alpine',
                name='Alpine',
                name_std='Alpine',
                country=self.country,
                region=self.region,
                location=Point(-116.76641,32.83505),
                population=14236,
                elevation=559,
                kind='PPL',
                timezone='America/Los_Angeles',
            )
        self.city.save()
        self.id = 8227
        self.airport_defaults = dict(
                name='On the Rocks Airport',
                city_name='Alpine',
                iata=None,
                icao='1CA6',
                local='1CA6',
                ident='1CA6',
                altitude=0.0,
                longitude=-116.7229995727539,
                latitude=32.76509857177734,
                country=self.country,
                region=self.region,
                city=self.city,
                type='small_airport'
            )

    def test_create_airport(self):
        country, region, city = get_location_info('Alpine', None, None, -116.7229995727539, 32.76509857177734)
        self.assertIsNotNone(country)
        self.assertIsNotNone(region)
        self.assertIsNotNone(city)
        airport = create_airport(id=self.id, **self.airport_defaults)
        self.assertIsNotNone(airport)

    def test_create_airport_no_name(self):
        country, region, city = get_location_info('', None, None, -116.7229995727539, 32.76509857177734)
        self.assertIsNotNone(country)
        self.assertIsNotNone(region)
        self.assertIsNotNone(city)
        defaults = self.airport_defaults
        defaults['name'] = ''
        airport = create_airport(id=self.id, **defaults)
        self.assertIsNotNone(airport)
        self.assertEqual(airport.name, 'Alpine')

    def test_create_airport_no_city_name(self):
        country, region, city = get_location_info('', None, None, -116.7229995727539, 32.76509857177734)
        self.assertIsNotNone(country)
        self.assertIsNotNone(region)
        self.assertIsNotNone(city)
        defaults = self.airport_defaults
        defaults['name'] = ''
        defaults['city_name'] = ''
        airport = create_airport(id=self.id, **defaults)
        self.assertIsNotNone(airport)
        self.assertEqual(airport.name, 'Alpine')

class TestAirports1(TestCase):
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
            id=1,
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
        self.assertIsNotNone(self.sut.id)
        self.assertIsNotNone(self.sut.name)
        self.assertIsNotNone(self.sut.iata)
        self.assertIsNotNone(self.sut.icao)
        self.assertIsNotNone(self.sut.altitude)
        self.assertIsNotNone(self.sut.location)
        self.assertIsNotNone(self.sut.country)
        self.assertIsNotNone(self.sut.city)

    def tearDown(self):
        pass
