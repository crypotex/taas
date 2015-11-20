# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0002_change_field_name_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('type', models.CharField(choices=[('TR', 'Transaction'), ('BU', 'Budget'), ('ST', 'Staged')], max_length=2)),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], decimal_places=2)),
                ('date_created', models.DateTimeField(verbose_name='date created', default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='field',
            name='cost',
            field=models.DecimalField(verbose_name='cost', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)], decimal_places=2),
        ),
        migrations.AddField(
            model_name='reservation',
            name='payment',
            field=models.ForeignKey(verbose_name='Payment', to='reservation.Payment', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
