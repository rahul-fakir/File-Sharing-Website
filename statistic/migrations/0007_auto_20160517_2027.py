# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-17 20:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0006_auto_20160517_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editshtml',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 17, 20, 27, 16, 943128)),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 17, 20, 27, 16, 942485)),
        ),
    ]