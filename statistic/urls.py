# coding: utf8
from django.conf.urls import url, patterns
from statistic import views

urlpatterns = patterns('',
    # ex: /Lending/
    url(r'^add/$', views.add, name='statistic.add'),
    url(r'^opensAjax/$', views.opensAjax, name="statistic.opensAjax"),
)
