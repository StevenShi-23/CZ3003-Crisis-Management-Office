# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CMOBackend', '0002_auto_20171011_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='PlanID',
        ),
        migrations.AddField(
            model_name='plan',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]