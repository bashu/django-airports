# -*- coding: utf-8 -*-

import csv
import itertools
import logging
import os
import sys
from optparse import make_option

import django
import requests
from cities.models import Country, City
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from tqdm import tqdm

from airports.models import Airport

ENDPOINT_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"

"""
Maximum distance used to filter out too distant cities.
"""
MAX_DISTANCE_KM = 200

APP_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

logger = logging.getLogger("airports")


def get_airport(airport_id, longitude, latitude, name, iata, icao, altitude, city, country):
    """

    :param airport_id:
    :param longitude:
    :param latitude:
    :param name:
    :param iata:
    :param icao:
    :param altitude:
    :param city:
    :param country:
    :return:
    """
    point = Point(longitude, latitude, srid=4326)

    name = name or city.name

    if icao == r'\N':
        icao = ''
    try:
        altitude = round(altitude * 0.3048, 2)
    except Exception:
        altitude = 0.0

    airport, created = Airport.objects.get_or_create(
        iata=iata, icao=icao, name=name, airport_id=airport_id,
        altitude=altitude, location=point, country=country, city=city,
    )
    if created:
        logger.debug("Added airport: %s", airport)
    return airport


def get_country(name, city):
    """

    :param name:
    :param city:
    :return:
    """

    qs_all = Country.objects.all()

    qs = qs_all.filter(name__iexact=name)  # first attempt
    if qs.count() == 1:
        return qs.first()

    qs = qs_all.filter(alt_names__name__iexact=name)  # second attempt
    if qs.count() == 1:
        return qs.first()

    if city is not None:
        qs = qs_all.filter(cities=city)
        if qs.count() >= 1:
            return qs.first()  # third attempt

    return None


def get_city(name, latitude, longitude):
    """

    :param name:
    :param latitude:
    :param longitude:
    :return: None if something wrong.
    """

    point = Point(latitude, longitude, srid=4326)

    qs_all = City.objects.all()

    qs = qs_all.filter(name_std__iexact=name)
    if qs.count() == 1:
        return qs.first()

    qs = qs_all.filter(Q(name__iexact=name) | Q(alt_names__name__iexact=name))
    if qs.count() == 1:
        return qs.first()

    qs = qs_all.all() \
        .annotate(distance=Distance('location', point)) \
        .filter(distance__lte=MAX_DISTANCE_KM * 1000) \
        .order_by('distance').all()

    if qs.count() >= 1:
        return qs.first()
    else:
        return None


class Command(BaseCommand):
    data_dir = os.path.join(APP_DIR, 'data')

    default_format = 'airport_id,name,city_name,country_name,iata,icao,latitude,longitude,altitude,timezone,dst'

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

    def handle(self, *args, **options):
        logger.info('Checking countries and cities')
        if City.objects.all().count() == 0 or Country.objects.all().count() == 0:
            call_command('cities', '--import', 'country,city')

        self.options = options

        if self.options['flush'] is True:
            self.flush_airports()
        else:
            columns = self.default_format.split(',')
            columns = dict(list(zip(columns, itertools.count())))

            with open(self.download(), 'rt') as f:
                self.stdout.flush()
                try:
                    importer = DataImporter(columns, self.stdout, self.stderr)
                except Exception:
                    raise CommandError('Can not continue processing')

                importer.start(f)

    def download(self, filename='airports.dat'):
        logger.info("Downloading: " + filename)
        response = requests.get(ENDPOINT_URL, data={})

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


class DataImporter(object):
    def __init__(self, columns, stdout=sys.stdout, stderr=sys.stderr):
        self.columns = columns
        self.stdout = stdout
        self.stderr = stderr

    def start(self, f):
        columns = self.columns

        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)

        for row in tqdm([r for r in reader],
                        desc="Importing Airports"
                        ):
            airport_id = row[columns['airport_id']]
            latitude = float(row[columns['latitude']])
            longitude = float(row[columns['longitude']])
            city_name = row[columns['city_name']]
            country_name = row[columns['country_name']]

            name = row[columns['name']].strip()
            iata = row[columns['iata']].strip()
            icao = row[columns['icao']].strip()

            altitude = int(row[columns['altitude']].strip())

            if Airport.objects.filter(airport_id=airport_id).all().count() == 0:
                city = get_city(city_name, latitude=latitude, longitude=longitude)
                if city is None:
                    logger.warning(
                        'Airport: {name}: Cannot find city: {city_name}.'.format(name=name, city_name=city_name))

                country = get_country(country_name, city)
                if country is None:
                    logger.warning(
                        'Airport:  {name}: Cannot find country: {country_name}'\
                            .format(name=name, country_name=country_name))

                airport = get_airport(airport_id, longitude, latitude, name, iata, icao, altitude, city, country)
