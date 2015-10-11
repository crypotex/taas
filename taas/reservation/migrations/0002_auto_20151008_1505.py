# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_create_reservation_and_field_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='payment_sum',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='timeslot',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(8), django.core.validators.MaxValueValidator(21)]),
        ),
    ]
