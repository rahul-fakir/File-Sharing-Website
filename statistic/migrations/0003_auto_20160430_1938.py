# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 19:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0002_auto_20160428_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editshtml',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 30, 19, 38, 20, 941995)),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 30, 19, 38, 20, 941414)),
        ),
        migrations.AlterField(
            model_name='visitors',
            name='date',
            field=models.DateField(default=datetime.date(2016, 4, 30)),
        ),
    ]
