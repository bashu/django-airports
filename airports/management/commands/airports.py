# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import csv
import sys
import logging
import requests
import itertools

from optparse import make_option

from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError

from cities.models import Country, City

from ...models import Airport

ENDPOINT_URL = "https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airports.dat?format=raw"

APP_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

logger = logging.getLogger("airports")


class Command(BaseCommand):
    data_dir = os.path.join(APP_DIR, 'data')

    default_format = 'airport_id,name,city_name,country_name,iata,icao,latitude,longitude,altitude,timezone,dst'

    help = """Imports airport data from CSV into DB, complementing it with country/city information"""
    option_list = BaseCommand.option_list + (
        make_option('--flush', action='store_true', default=False,
            help="Flush airport data."
        ),
    )

    def handle(self, *args, **options):
        self.options = options

        if self.options['flush'] is True:
            self.flush_airports()
        else:
            columns = self.default_format.split(',')
            columns = dict(itertools.izip(columns, itertools.count()))

            try:
                with open(self.download(), 'rb') as f:
                    self.stdout.flush()
                    try:
                        importer = DataImporter(columns, self.stdout, self.stderr)
                    except Exception:
                        raise CommandError('Can not continue processing')

                    importer.start(f)
            except IOError as e:
                raise CommandError('Can not open file: {0}'.format(e))

    def download(self, filename='airports.dat'):
        logger.info("Downloading: " + filename)        
        response = requests.post(ENDPOINT_URL, data={})

        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        fobj = open(filepath, 'w')
        fobj.write(response.text.encode('utf-8'))
        fobj.close()

        return filepath

    def flush_airports(self):
        logger.info("Flushing airports data")
        Airport.objects.all().delete()


class DataImporter(object):

    def __init__(self, columns, stdout=sys.stdout, stderr=sys.stderr):
        self.columns = columns
        self.stdout = stdout
        self.stderr = stderr

        self.countries = self.cities = {}  # cache
        self.saved_airports = set()

    def start(self, f, encoding='utf8'):
        logger.info("Importing airport data")
        columns = self.columns

        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        if encoding:
            try:
                f.readline().decode(encoding)
            except UnicodeDecodeError as e:
                raise Exception('Invalid encoding: {0}'.format(encoding))
        f.seek(0)
        reader = csv.reader(f, dialect)

        rows = 0
        for row in reader:
            try:
                if (encoding):
                    row = map(lambda c: c.decode(encoding), row)

                iata = row[columns['iata']]
                if not iata:
                    continue  # skip airports without IATA code

                if iata in self.saved_airports:
                    continue  # already saved

                country = self.get_country(row[columns['country_name']], row)
                if not bool(country): 
                    logger.warning("Airport: {0}: Cannot find country: {1} -- skipping".format(
                        row[columns['name']], row[columns['country_name']]))
                    continue  # unable to get related country

                city = self.get_city(row[columns['city_name']], row, country)
                if not bool(city):
                    logger.warning("Airport: {0}: Cannot find city: {1} -- skipping".format(
                        row[columns['name']], row[columns['city_name']]))
                    continue  # unable to get related city

                airport = self.get_airport(iata, row, city)
                if not airport:
                    continue

                logger.debug("Added airport: {0}".format(airport))

                if iata not in self.saved_airports:
                    self.saved_airports.add(iata)

                rows += 1
            except IndexError as e:
                pass

    def get_country(self, name, row):
        cols, cache = self.columns, self.countries

        if name in cache:
            return cache[name]

        point = Point(float(row[cols['longitude']]), float(row[cols['latitude']]))
        qs = Country.objects.all()

        try:
            c = qs.get(Q(name__iexact=name) | Q(alt_names__name__iexact=name))  # first attempt
        except (Country.DoesNotExist, MultipleObjectsReturned):
            try:
                c = qs.filter(city__in=City.objects.filter(
                    location__distance_lte=(point, D(km=25))))[0]  # second attempt
            except KeyError:
                c = None  # shit happens

        cache[name] = c
        return c

    def get_city(self, name, row, country):
        cols, cache = self.columns, self.cities

        iso = country.code
        if (iso, name) in cache:
            return cache[(iso, name)]

        point = Point(float(row[cols['longitude']]), float(row[cols['latitude']]))
        qs = City.objects.distance(point).filter(country=country)

        try:
            c = qs.get(Q(name_std__iexact=name) | Q(name__iexact=name) | Q(alt_names__name__iexact=name))
        except (City.DoesNotExist, MultipleObjectsReturned):
            try:
                c = qs.exclude(
                    location__distance_gte=(point, D(km=50))).order_by('distance')[0]
            except IndexError:
                c = None

        cache[(iso, name)] = c
        return c

    def get_airport(self, iata, row, city):
        cols = self.columns

        try:
            return Airport.objects.get(code=iata)
        except Airport.DoesNotExist:
            pass

        point = Point(float(row[cols['longitude']]), float(row[cols['latitude']]))
        name = row[cols['name']] or city.name

        return Airport.objects.create(
            code=iata, name=name, location=point, country=city.country, city=city)
