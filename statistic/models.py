from __future__ import unicode_literals
import datetime
from django.db import models

class visitors(models.Model):
    ip = models.CharField(max_length=20)
    date = models.DateField(default=datetime.date.today())


class Statistic(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now())
    edits = models.BooleanField(default=False)


class editsHtml(models.Model):
    date = models.DateTimeField(default=datetime.datetime.today())
    user = models