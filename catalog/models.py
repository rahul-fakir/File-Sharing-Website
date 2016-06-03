    # coding: utf-8
from __future__ import unicode_literals
import datetime
from django.db import models
from cab.models import ExtUser
from django.core.urlresolvers import reverse


class fotos(models.Model):
    name = models.CharField(max_length=200)
    path = models.FileField(
        upload_to='media/fotos/', blank=True, null=True    
    )

class Libraries(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(fotos)
    
    def __unicode__(self):
        return self.name


class item(models.Model):
    name = models.CharField(max_length=100)
    date_published = models.DateTimeField(default=datetime.datetime.now())
    main_foto = models.ForeignKey(fotos)
    foto = models.TextField() # CSV format ';' values=[id_f, id_f, id_f]
    information = models.TextField()
    views = models.IntegerField(default=0)
    tags = models.TextField() # CSV format ';' values=[tag, tag, tag]
    user = models.ForeignKey(ExtUser)
    library = models.ForeignKey(Libraries, null=True, blank=True)
    
    
class like(models.Model):
    user = models.ForeignKey(ExtUser)
    item = models.ForeignKey(item)
    
    
class file(models.Model):
    name = models.CharField(max_length=150)
    dowloads = models.IntegerField(default=0)
    size = models.FloatField(default=0.0)
    date_published = models.DateTimeField(
        default=datetime.datetime.now()    
    )
    f = models.FileField(
        upload_to='media/files/', blank=True, null=True 
    )
    item = models.ForeignKey(item)
    
class Categories(models.Model):
    name = models.CharField(max_length=220)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(default="http://www.google.com")
    
    def __unicode__(self):
        return "{}".format(self.name)