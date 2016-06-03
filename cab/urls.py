from django.conf.urls import url, patterns, include
from django.contrib.auth import views as auth_views
import cab.views

urlpatterns = patterns('',
                       # ex: /cab Klients/
                       url(r'^$', cab.views.main, name="cab.main"),
    url(r'^downloadAvatar/$', cab.views.downloadAvatar, name="cab.downloadAvatar"),
    url(r'^downloadFilesNewItem/$', cab.views.downloadFilesNewItem, name="cab.downloadFilesNewItem"),
    url(r'^saveAvatar/$', cab.views.saveAvatar, name="cab.saveAvatar"),
    url(r'^editProfile/$', cab.views.editProfile, name="cab.editProfile"),
    url(r'^addItem/$', cab.views.addItem, name="cab.addItem"),
    url(r'^registerPost/$', cab.views.registerPost, name="cab.registerPost"),
    url(r'^deleteItem/$', cab.views.deleteItem, name="cab.deleteItem"),
    url(r'^addDownloadFile/$', cab.views.addDownloadFile, name="cab.addDownloadFile"),
    url(r'^addDownloadFileAll/$', cab.views.addDownloadFileAll, name="cab.addDownloadFileAll"),
    url(r'^search/$', cab.views.search, name="search"),
    url(r'^like/$', cab.views._like, name="like"),
    url(r'^ajaxOpens/$', cab.views.ajaxOpens, name="ajaxOpens"),
    url(r'^changePassword/$', cab.views.changePassword, name="cab.changePassword"),
    url(r'^change/$', cab.views.changeItem, name="cab.changeItem"),
    url(r'^changeDelFoto/$', cab.views.changeDelFoto, name="cab.changeDelFoto"),
    url(r'^changeAddFoto/$', cab.views.changeAddFoto, name="cab.changeAddFoto"),
    url(r'^changeTags/$', cab.views.changeTags, name="cab.changeTags"),
    url(r'^changeLibrary/$', cab.views.changeLibrary, name="cab.changeLibrary"),
    url(r'^changeInform/$', cab.views.changeInform, name="cab.changeInform"),
    url(r'^changeDelFile/$', cab.views.changeDelFile, name="cab.changeDelFile"),
    #url(r'^changeAddFile/$', cab.views.changeAddFile, name="cab.changeAddFile"),
    url(r'^changeAddFileSave/$', cab.views.changeAddFileSave, name="cab.changeAddFileSave"),
)