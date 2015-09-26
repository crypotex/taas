# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.auth.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=30, unique=True, error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?\\d{5,15}$', message='Phone number is invalid.')], verbose_name='phone number', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=False, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', verbose_name='groups', blank=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission', verbose_name='user permissions', blank=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
