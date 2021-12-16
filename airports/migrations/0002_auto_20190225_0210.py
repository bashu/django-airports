# Generated by Django 2.1.7 on 2019-02-25 10:10

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cities", "0011_auto_20180108_0706"),
        ("airports", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="airport",
            name="city_name",
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="name"),
        ),
        migrations.AddField(
            model_name="airport",
            name="ident",
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name="Ident code"),
        ),
        migrations.AddField(
            model_name="airport",
            name="local",
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name="Local code"),
        ),
        migrations.AddField(
            model_name="airport",
            name="region",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="cities.Region"),
        ),
        migrations.AddField(
            model_name="airport",
            name="type",
            field=models.CharField(default="", max_length=16),
        ),
        migrations.AlterField(
            model_name="airport",
            name="iata",
            field=models.CharField(
                blank=True,
                max_length=3,
                null=True,
                validators=[django.core.validators.MinLengthValidator(3)],
                verbose_name="IATA/FAA code",
            ),
        ),
        migrations.AlterField(
            model_name="airport",
            name="icao",
            field=models.CharField(
                blank=True,
                max_length=4,
                null=True,
                validators=[django.core.validators.MinLengthValidator(4)],
                verbose_name="ICAO code",
            ),
        ),
    ]
