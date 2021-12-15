from cities.models import Country, City, Region
from django.contrib.gis.geos import Point
from django.test import TestCase

from airports.management.commands.airports import get_location_info, create_airport
from airports.models import Airport

# python 2&3 compatible
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


class TestCommandAirports3(TestCase):
    def setUp(self):
        default_format = 'airport_id,name,city_name,country_name,iata,icao,latitude,longitude,altitude,timezone,dst'

        twolines = """1,"Goroka Airport","Goroka","Papua New Guinea","GKA","AYGA",-6.081689834590001,145.391998291,5282,10,"U","Pacific/Port_Moresby","airport","OurAirports"
        2,"Madang Airport","Madang","Papua New Guinea","MAG","AYMD",-5.20707988739,145.789001465,20,10,"U","Pacific/Port_Moresby","airport","OurAirports" """

        self.columns = default_format.split(',')
        self.csv = StringIO(twolines)

        self.dialect = csv.Sniffer().sniff(self.csv.read(512))

        self.csv.seek(0)
        self.reader = csv.DictReader(self.csv, dialect=self.dialect, fieldnames=self.columns)

        self.url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"

    def test_get_lines(self):
        lines = get_lines(self.url)

        self.assertTrue(len(next(lines)) > 10)
        self.assertTrue(len(next(lines)) > 10)
        self.assertTrue(len(next(lines)) > 10)

    def test_read_airports(self):
        airports = list(read_airports(self.reader))
        self.assertEquals(len(airports), 2)

    def test_airports_updated(self):
        # read them in first
        list(read_airports(self.reader))

        self.assertEquals(Airport.objects.count(), 2)
        self.assertEqual(Airport.objects.get(airport_id=1).name, "Goroka Airport")
        self.assertEqual(Airport.objects.get(airport_id=2).name, "Madang Airport")

        # update the airports
        csv_text = StringIO("""1,"Goro White Dog Airport","Goroka","Papua New Guinea","GKA","AYGA",-6.081689834590001,145.391998291,5282,10,"U","Pacific/Port_Moresby","airport","OurAirports"
        2,"Vabank Airport","Madang","Papua New Guinea","MAG","AYMD",-5.20707988739,145.789001465,20,10,"U","Pacific/Port_Moresby","airport","OurAirports" """)
        reader = csv.DictReader(csv_text, dialect=self.dialect, fieldnames=self.columns)

        list(read_airports(reader))

        self.assertEquals(Airport.objects.count(), 2)
        self.assertEqual(Airport.objects.get(airport_id=1).name, "Goro White Dog Airport")
        self.assertEqual(Airport.objects.get(airport_id=2).name, "Vabank Airport")


class TestCommandAirports(TestCase):
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
        self.airport = Airport(
                id=8227,
                name='On the Rocks Airport',
                city_name='Alpine',
                iata=None,
                icao='1CA6',
                local='1CA6',
                ident='1CA6',
                altitude=0.0,
                location=Point(-116.7229995727539,32.76509857177734),
                country=self.country,
                region=self.region,
                city=self.city,
                type='small_airport'
            )
        self.airport.save()

    def assert_location_tuple(self, country, region, city):
        self.assertEqual(country, self.country)
        self.assertEqual(region, self.region)
        self.assertEqual(city, self.city)

    def test_get_location_info_name(self):
        country, region, city = get_location_info('Alpine', None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_wrong_name(self):
        country, region, city = get_location_info('Wrong Name', None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_fix_name(self):
        country, region, city = get_location_info('', None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_missing_name(self):
        country, region, city = get_location_info('', None, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_country(self):
        country, region, city = get_location_info('', self.country, None, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_country_region(self):
        country, region, city = get_location_info('', self.country, self.region, -116.7229995727539, 32.76509857177734)
        self.assert_location_tuple(country, region, city)

    def test_get_location_info_country_region_bad_coords(self):
        country, region, city = get_location_info('', self.country, self.region, -116.7, 38.0)
        self.assertEqual(country, self.country)
        self.assertEqual(region, self.region)
        self.assertIsNone(city)

    def test_get_location_info_country_bad_coords(self):
        country, region, city = get_location_info('', self.country, None, -106.0, 32.0)
        self.assertEqual(country, self.country)
        self.assertIsNone(region)
        self.assertIsNone(city)


class TestCommandAirports1(TestCase):
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
        country, region, city = get_location_info('test', None, None, 1000, -1000)
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
                None, None, self.airport_location.coords[0], self.airport_location.coords[1])
        self.assertIsNotNone(city)
        self.assertIsNotNone(country)
        self.assertEqual(country, self.guinea)
