# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(verbose_name='name', unique=True, max_length=10),
        ),
    ]
