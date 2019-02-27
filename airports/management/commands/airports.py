# -*- coding: utf-8 -*-

"""
Download airports file from ourairports.org, and import to database
The airports csv file fieldnames are these:
    fieldnames = (
        'id', 'ident', 'type', 'name', 'latitude_deg', 'longitude_deg',
        'elevation_ft', 'continent', 'iso_country', 'iso_region',
        'municipality', 'scheduled_service', 'gps_code', 'iata_code',
        'local_code', 'home_link', 'wikipedia_link', 'keywords',
    )
"""

import csv
import itertools
import logging
import os
import pprint
import re
import sys
from optparse import make_option
from collections import defaultdict

import django
import requests
from cities.models import Country, Region, City
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from tqdm import tqdm

from airports.models import Airport

ENDPOINT_URL = 'http://ourairports.com/data/airports.csv'
DIVISIONS_URL = 'https://raw.githubusercontent.com/Tigrov/geoname-divisions/master/result/divisions.csv'

# Maximum distance used to filter out too-distant cities.
MAX_DISTANCE_KM = 200

APP_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

logger = logging.getLogger("airports")


class Command(BaseCommand):
    data_dir = os.path.join(APP_DIR, 'data')

    help = """Imports airport data from CSV into DB, complementing it with country/city information"""
    if django.VERSION < (1, 8):
        option_list = BaseCommand.option_list + (
            make_option('--flush', action='store_true', default=False,
                        help="Flush airports data."
                        ),
        )

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            default=False,
            help="Flush airports data."
        )
        parser.add_argument(
            '--update',
            action='store_true',
            default=False,
            help="Force update of existing airports."
        )

    def handle(self, *args, **options):
        logger.info('Checking countries and cities')
        if City.objects.all().count() == 0 or Country.objects.all().count() == 0:
            call_command('cities', '--import', 'country,city')

        self.options = options

        if self.options['flush'] is True:
            self.flush_airports()
        else:
            #with open('{}/airports.dat'.format(self.data_dir), 'rt') as f:
            divisions_file  = self.download(DIVISIONS_URL, filename='divisions.dat')
            with open(divisions_file, 'rt') as f:
                self.divisions = DivisionImporter(division_file=f,
                        stdout=self.stdout,
                        stderr=self.stderr).division_dict

            airport_file  = self.download(ENDPOINT_URL, filename='airports.dat')
            with open(airport_file, 'rt') as f:
                self.stdout.flush()
                try:
                    importer = DataImporter(divisions=self.divisions,
                            update=self.options['update'],
                            stdout=self.stdout,
                            stderr=self.stderr)
                except Exception:
                    raise CommandError('Can not continue processing')

                importer.start(f)

    def download(self, url, filename='airports.dat'):
        logger.info("Downloading: " + filename)
        response = requests.get(url, data={})

        if response.status_code != 200:
            response.raise_for_status()

        try:
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)

            fobj = open(filepath, 'wb')
            fobj.write(response.text.encode('utf-8'))
            fobj.close()

            return filepath

        except IOError as e:
            raise CommandError('Can not open file: {0}'.format(e))

    def flush_airports(self):
        logger.info("Flushing airports data")
        Airport.objects.all().delete()

class DivisionImporter(object):
    def __init__(self, division_file=None, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.division_dict = defaultdict(dict)

        dialect = csv.Sniffer().sniff(division_file.read(1024))
        division_file.seek(0)
        reader = csv.DictReader(division_file, dialect=dialect)

        for row in tqdm(list(reader), desc="Processing Divisions"):
            country_code = row['ISO-3166-1']
            region_code = row['ISO-3166-2']
            fips = row['Fips']
            GN = row['GN']
            self.division_dict[country_code][region_code] = dict(fips=fips, GN=GN)

class DataImporter(object):
    def __init__(self, divisions=None, update=False, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.divisions = divisions
        self.update = update

    def start(self, f):
        regex_delete = re.compile(r'(^delete|deleted|\[DELETE\])', re.IGNORECASE)
        regex_region = re.compile(r'[-/]')

        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)

        reader = csv.DictReader(f, dialect=dialect)

        for row in tqdm(list(reader), desc="Importing Airports"):
            airport_id = row['id']
            latitude = float(row['latitude_deg'])
            longitude = float(row['longitude_deg'])
            city_name = row['municipality'] or None
            row_country_code = row['iso_country']
            country_code, region_code = regex_region.split(row['iso_region'].strip(), 1)
            if not row_country_code == country_code:
                raise CommandError('Country mismatch: {} != {}'.format(row_country_code, country_code))

            name = row['name'].strip() or None
            type = row['type'].strip() or None
            ident = row['ident'].strip() or None
            local = row['local_code'].strip() or None
            iata = row['iata_code'].strip() or None
            icao = row['gps_code'].strip() or None

            altitude = row['elevation_ft'].strip()

            # Filter out ones we know we don't need, including SPAM entries.
            if ((latitude == 0 and longitude == 0) or
                type == 'closed' or
                country_code.startswith('ZZ') or
                regex_delete.match(name)):
                continue

            if not Airport.objects.filter(airport_id=airport_id).exists() or self.update:
                try:
                    country = Country.objects.get(code=country_code)
                except Country.DoesNotExist:
                    # That's bad!  But still recoverable by reverse geocoding
                    logger.error('Bad country_code: {} == {}'.format(row['iso_country'], country_code))
                    country = None

                # First try to find region by given region_code.  This is a lot faster
                # than looking it up based on its coordinates, which is our fallback.
                try:
                    region = Region.objects.get(country=country, code=region_code)
                except Region.DoesNotExist:
                    try:
                        assert self.divisions
                        fips_code = self.divisions[country_code][region_code]['fips']
                        gn_code = self.divisions[country_code][region_code]['GN']
                        regions = Region.objects.filter(Q(country=country) & (Q(code=fips_code) | Q(code=gn_code)))
                        assert regions.count() == 1
                        region = regions.first()
                    except (AssertionError, KeyError, Region.DoesNotExist):
                        # Unable to parse the region code, but may be able to figure it
                        # out by finding out where the lat/lng is located...
                        logger.debug('Bad region_code: {}'.format(row['iso_region']))
                        region = None

                country, region, city = get_location_info(city_name, country, region, latitude, longitude)

                if city is None:
                    logger.debug(
                        'Airport: {name}: Cannot find city: {city_name}.'.format(name=name, city_name=city_name))

                airport = create_airport(
                    airport_id=airport_id,
                    altitude=altitude,
                    city=city,
                    city_name=city_name,
                    country=country,
                    iata=iata,
                    icao=icao,
                    ident=ident,
                    latitude=latitude,
                    local=local,
                    longitude=longitude,
                    name=name,
                    region=region,
                    type=type,
                )

def create_airport(
        airport_id=None, type=None, altitude=None,
        name=None, city=None, city_name=None, region=None, country=None,
        iata=None, icao=None, ident=None, local=None,
        latitude=None, longitude=None,
        ):

    """
    Get or create an Airport.

    :param airport_id:
    :param type:
    :param longitude:
    :param latitude:
    :param name:
    :param city_name:
    :param iata:
    :param icao:
    :param ident:
    :param local:
    :param altitude:
    :param city:
    :param region:
    :param country:
    :return:
    """
    location = Point(longitude, latitude, srid=4326)

    name = name or city_name or getattr(city, 'name', 'UNKNOWN')

    try:
        altitude = round(altitude * 0.3048, 2)
    except TypeError:
        altitude = 0.0

    defaults = dict(
        altitude=altitude,
        city=city,
        city_name=city_name,
        country=country,
        iata=iata,
        icao=icao,
        ident=ident,
        local=local,
        location=location,
        name=name,
        region=region,
        type=type
    )

    try:
        airport, created = Airport.objects.update_or_create(
            airport_id=airport_id,
            defaults=defaults
        )
        if created:
            logger.debug("Added airport: %s", airport)
        return airport

    except Exception as e:
        logger.error('{}: id={}\n{}'.format(
            e, airport_id, pprint.pformat(defaults))
        )

    return None


def get_location_info(name, country, region, latitude, longitude):
    """
    Get location info for an airport given incomplete information.

    :param name:
    :param country:
    :param region:
    :param latitude:
    :param longitude:
    :return: (country, region, city)
    """

    if country:
        if region:
            filtered_cities = City.objects.filter(region=region)
        else:
            filtered_cities = City.objects.filter(country=country)
    else:
        filtered_cities = City.objects.all()

    qs = filtered_cities.filter(name_std__iexact=name)
    if qs.count() == 1:
        city = qs.first()
        return city.country, city.region, city

    qs = filtered_cities.filter(Q(name__iexact=name) | Q(alt_names__name__iexact=name))
    if qs.count() == 1:
        city = qs.first()
        return city.country, city.region, city

    # If we didn't find the city by name, return the city in the same country/region
    # which is closest to the given lng/lat.
    point = Point(longitude, latitude, srid=4326)
    qs = filtered_cities \
        .annotate(distance=Distance('location', point)) \
        .filter(distance__lte=MAX_DISTANCE_KM * 1000) \
        .order_by('distance')

    if qs.count() >= 1:
        city = qs.first()
        return city.country, city.region, city

    return country, region, None
