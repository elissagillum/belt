# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-04 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180304_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='task_status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Done'), (2, 'Missed')], default='PENDING'),
        ),
    ]
