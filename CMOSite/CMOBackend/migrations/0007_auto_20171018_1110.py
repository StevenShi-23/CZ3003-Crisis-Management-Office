# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMOBackend', '0006_crisis_crisisid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crisis',
            name='Cleared',
        ),
        migrations.AddField(
            model_name='crisis',
            name='CrisisStatus',
            field=models.CharField(choices=[('NC', 'New Crisis, Awaiting Plan'), ('PA', 'Plan In Action'), ('PF', 'Plan Formed, Awaiting Authorization'), ('PAG', 'Approved by General, Awaiting Authorization'), ('CO', 'Crisis Cleared'), ('PAP', 'Authorized, Awaiting Activation'), ('UP', 'New Update Received')], default='NC', max_length=3),
        ),
    ]
