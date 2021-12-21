from cities.models import City, Country, Region
from django.contrib.gis.geos import Point
from django.test import TestCase

from airports.management.commands.airports import get_location_info
from airports.models import Airport


class ManagementCommandTests(TestCase):
    def setUp(self):
        self.country = Country(
            slug="United-States",
            name="United States",
            code="US",
            code3="USA",
            population=310232863,
            area=9629091,
            currency="USD",
            currency_name="Dollar",
            currency_symbol="$",
            language_codes="en-US,es-US,haw,fr",
            phone="1",
            tld="us",
            capital="Washington",
        )
        self.country.save()
        self.region = Region(
            slug="California_US.CA",
            name="California",
            name_std="California",
            code="CA",
            country=self.country,
        )
        self.region.save()
        self.city = City(
            slug="5323401-Alpine",
            name="Alpine",
            name_std="Alpine",
            country=self.country,
            region=self.region,
            location=Point(-116.76641, 32.83505),
            population=14236,
            elevation=559,
            kind="PPL",
            timezone="America/Los_Angeles",
        )
        self.city.save()
        self.airport = Airport(
            id=8227,
            name="On the Rocks Airport",
            city_name="Alpine",
            iata=None,
            icao="1CA6",
            local="1CA6",
            ident="1CA6",
            altitude=0.0,
            location=Point(-116.7229995727539, 32.76509857177734),
            country=self.country,
            region=self.region,
            city=self.city,
            type="small_airport",
        )
        self.airport.save()

    def assert_location_tuple(self, country, region, city):
        self.assertEqual(country, self.country)
        self.assertEqual(region, self.region)
        self.assertEqual(city, self.city)

    def test_get_location_info_name(self):
        country, region, city = get_location_info("Alpine", None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_wrong_name(self):
        country, region, city = get_location_info("Wrong Name", None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_fix_name(self):
        country, region, city = get_location_info("", None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_missing_name(self):
        country, region, city = get_location_info("", None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_country(self):
        country, region, city = get_location_info("", self.country, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_country_region(self):
        country, region, city = get_location_info("", self.country, self.region, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_country_region_bad_coords(self):
        country, region, city = get_location_info("", self.country, self.region, -116.7, 38.0)
        self.assertEqual(country, self.country)
        self.assertEqual(region, self.region)
        self.assertIsNone(city)

    def test_get_location_info_country_bad_coords(self):
        country, region, city = get_location_info("", self.country, None, -106.0, 32.0)
        self.assertEqual(country, self.country)
        self.assertIsNone(region)
        self.assertIsNone(city)
