# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_auto_20151008_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='timeslot',
            field=models.SmallIntegerField(verbose_name='timeslot', validators=[django.core.validators.MinValueValidator(8), django.core.validators.MaxValueValidator(8)]),
        ),
    ]
