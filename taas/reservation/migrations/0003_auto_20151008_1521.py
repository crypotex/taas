# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20151008_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='timeslot',
            field=models.TimeField(verbose_name='timeslot'),
        ),
    ]
