# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taas.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', taas.user.models.CustomUserManager()),
            ],
        ),
    ]
