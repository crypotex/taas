# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_budget_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='button_id',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Button ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='pin',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='pin'),
        ),
    ]
