# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airport_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('iata', models.CharField(blank=True, max_length=3, verbose_name='IATA/FAA code', validators=[django.core.validators.MinLengthValidator(3)])),
                ('icao', models.CharField(blank=True, max_length=4, verbose_name='ICAO code', validators=[django.core.validators.MinLengthValidator(4)])),
                ('altitude', models.FloatField(default=0, verbose_name='altitude')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='location')),
                ('city', models.ForeignKey(to='cities.City')),
                ('country', models.ForeignKey(to='cities.Country')),
            ],
            options={
                'ordering': ['iata'],
            },
            bases=(models.Model,),
        ),
    ]
