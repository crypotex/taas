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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=1, verbose_name='field', unique=True)),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='cost')),
                ('description', models.TextField(verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateField(verbose_name='date')),
                ('timeslot', models.TimeField(verbose_name='timeslot')),
                ('payment_sum', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='payment sum')),
                ('method', models.IntegerField(choices=[(1, 'Payment made with bank link.'), (2, 'Payment made with existing budget')])),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('fields', models.ManyToManyField(to='reservation.Field')),
                ('user', models.ForeignKey(related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reservation',
                'verbose_name_plural': 'reservations',
            },
        ),
    ]
