# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_add_budget_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='budget',
            field=models.DecimalField(default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], decimal_places=2, verbose_name='budget (€)'),
        ),
    ]
