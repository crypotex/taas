# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, verbose_name='field', max_length=30)),
                ('cost', models.DecimalField(max_digits=5, decimal_places=2, verbose_name='cost', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('payed', models.BooleanField(verbose_name='Payed', default=False)),
                ('date_created', models.DateTimeField(verbose_name='date created', default=django.utils.timezone.now)),
                ('field', models.ForeignKey(to='reservation.Field', related_name='reservations')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='reservations')),
            ],
            options={
                'verbose_name_plural': 'reservations',
                'verbose_name': 'reservation',
            },
        ),
    ]
