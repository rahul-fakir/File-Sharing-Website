from django.conf.urls import patterns, url
from dashboard import views

urlpatterns = patterns('',
                       # ex: /cab Klients/
                       url(r'^$', views.main, name='test_main'))