from cities.models import Country, City, Region
from django.contrib.gis.geos import Point
from django.test import TestCase

from airports.management.commands.airports import get_location_info, create_airport
from airports.models import Airport


class TestCommandAirports(TestCase):
    def setUp(self):
        country = Country(
            name='country',
            population=0
        )
        country.save()
        region = Region(
            name_std='region',
            country=country
        )
        region.save()
        city1 = City(
            name='city1',
            name_std='city1....',
            country=country,
            region=region,
            location=Point(0, 0, srid=4326),
            population=0,
        )
        city1.save()
        self.city2 = City(
            name='city2',
            name_std='city2....',
            country=country,
            region=region,
            location=Point(100, 100, srid=4326),
            population=0,
        )
        self.city2.save()
        self.city3 = City(
            name='city3',
            name_std='city3....',
            country=country,
            region=region,
            location=Point(1000, -1000, srid=4326),
            population=0,
        )
        self.city3.save()

    def test_get_location_info(self):
        country, region, city = get_location_info('test', None, None, -1000, 1000)
        print(country, region, city)
        self.assertEqual(city, self.city3)

    def test_create_airport(self):
        pass

    def tearDown(self):
        pass


class TestCommandAirports2(TestCase):
    def setUp(self):
        self.guinea = Country.objects.create(
            name='Papua New Guinea',
            population=0,
            code='PG',
            code3='PNG',

        )
        self.city1 = City.objects.create(
            name='Goroka',
            name_std='Goroka',
            country=self.guinea,
            location=Point(145.38735, -6.08336, srid=4326),
            population=0,
        )

        country2 = Country.objects.create(
            name='Marshall Islands',
            population=0,
            code='MH',
            code3='MHL',
        )
        self.city2 = City.objects.create(
            name='Utrik',
            name_std='Utrik',
            country=country2,
            location=Point(169.84739, 11.22778, srid=4326),
            population=0,
        )
        self.airport_location = Point(146.725977, -6.569803, srid=4326)
        self.airport_region_name = 'Papua New Guinea'

    def test_get_location_info(self):
        country, region, city = get_location_info('test',
                None, None, self.airport_location.coords[1], self.airport_location.coords[0])
        self.assertIsNotNone(city)
        self.assertIsNotNone(country)
        self.assertEqual(country, self.guinea)
