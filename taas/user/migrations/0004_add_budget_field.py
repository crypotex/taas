# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_change_user_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='budget',
            field=models.PositiveIntegerField(default=0, verbose_name='budget (€)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(verbose_name='phone number', max_length=15, validators=[django.core.validators.RegexValidator(message='Phone number is invalid.', regex='^\\+?\\d{5,15}$')]),
        ),
    ]
