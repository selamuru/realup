# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 23:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('remanage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.UTC),
        ),
        migrations.AlterField(
            model_name='property',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.UTC),
        ),
    ]