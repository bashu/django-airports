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
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('code', models.CharField(max_length=3, serialize=False, verbose_name='IATA code', primary_key=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('city', models.ForeignKey(to='cities.City')),
                ('country', models.ForeignKey(to='cities.Country')),
            ],
            options={
                'ordering': ['code'],
            },
            bases=(models.Model,),
        ),
    ]
