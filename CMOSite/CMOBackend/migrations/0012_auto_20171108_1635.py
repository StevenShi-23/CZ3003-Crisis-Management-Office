# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMOBackend', '0011_auto_20171107_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='Status',
            field=models.CharField(max_length=255),
        ),
    ]
