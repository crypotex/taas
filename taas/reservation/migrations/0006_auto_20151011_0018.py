# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_auto_20151009_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(unique=True, max_length=30, verbose_name='field'),
        ),
    ]
