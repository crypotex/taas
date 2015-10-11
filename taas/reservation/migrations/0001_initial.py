# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='field')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='cost')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='date')),
                ('timeslot', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(8), django.core.validators.MaxValueValidator(21)], verbose_name='timeslot')),
                ('method', models.IntegerField(choices=[(1, 'Payment made with bank link.'), (2, 'Payment made with existing budget')], default=1)),
                ('date_created', models.DateTimeField(verbose_name='date created', default=django.utils.timezone.now)),
                ('fields', models.ManyToManyField(to='reservation.Field')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='reservations')),
            ],
            options={
                'verbose_name_plural': 'reservations',
                'verbose_name': 'reservation',
            },
        ),
    ]
