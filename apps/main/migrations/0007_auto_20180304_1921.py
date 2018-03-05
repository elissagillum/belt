# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-05 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20180304_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='task_status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Done'), (3, 'Missed')], default=1),
        ),
    ]