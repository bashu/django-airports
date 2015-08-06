# -*- coding: utf-8 -*-

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airports', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='airport',
            options={'ordering': ['airport_id']},
        ),
        migrations.AlterField(
            model_name='airport',
            name='airport_id',
            field=models.PositiveIntegerField(serialize=False, editable=False, primary_key=True),
        ),
    ]
