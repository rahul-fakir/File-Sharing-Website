from django.conf.urls import patterns, url
from about import views

urlpatterns = patterns('',
                       # ex: /cab Klients/
                       url(r'^$', views.main, name='about_main'))