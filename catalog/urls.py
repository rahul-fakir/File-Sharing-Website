from django.conf.urls import patterns, url
from catalog import views

urlpatterns = patterns('',
                       # ex: /cab Klients/
                       url(r'^$', views.main, name='catalog_main'),
                       url(r'^[0-9]*[/]+$', views.itemHtml, name='catalog_item'),
                       url(r'^libraries/$', views.libraries, name='libraries'),
                       url(r'^librarieslist/(?P<id>\d+)/$', views.libraries_detail, name='librariesdetail'),
                       url(r'^itemview/(?P<id>\d+)/$', views.itemHtmlFile, name='item_view_file'),
                       url(r'^viewfile/(?P<id>\d+)/$', views.showFile, name='showFile'),
            )