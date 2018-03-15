# Generated by Django 2.0.3 on 2018-03-14 18:17

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.CITIES_COUNTRY_MODEL),
        migrations.swappable_dependency(settings.CITIES_CITY_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airport_id', models.PositiveIntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('iata', models.CharField(blank=True, max_length=3, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='IATA/FAA code')),
                ('icao', models.CharField(blank=True, max_length=4, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='ICAO code')),
                ('altitude', models.FloatField(default=0, verbose_name='altitude')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='location')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.CITIES_CITY_MODEL)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.CITIES_COUNTRY_MODEL)),
            ],
            options={
                'ordering': ['airport_id'],
            },
        ),
    ]
