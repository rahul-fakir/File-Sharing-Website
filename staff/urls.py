from django.conf.urls import url
from staff import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.staff_login, name='staff-login'),
    url(r'^item$', views.item_view, name='item'),
    url(r'^item/(?P<pk>\d+)$', views.item_view_only, name='item_view_only'),
    url(r'^item/item_delete$', views.item_delete, name='item_delete'),
    url(r'^item/item_image_delete$', views.item_image_delete, name='item_image_delete'),
    url(r'^item/item_file_delete$', views.item_file_delete, name='item_file_delete'),
    url(r'^edit-profile/(?P<pk>\d+)$',
        views.edit_profile, name='edit-profile'),
    url(r'^user-info/$',
        views.user_info, name='user-info'),
    url(r'^change-password/$',
        views.change_password, name='change-password'),
    url(r'^change_avatar/(?P<user_id>\d+)/$',
        views.saveAvatar, name='saveavatar'),
    url(r'^categories$', views.categories, name='categories'),
    url(r'^categories-edit/(?P<pk>\d+)$', views.categories_edit, name='categories-edit'),
    url(r'^libraries$', views.libraries, name='libraries'),
    url(r'^libraries-edit/(?P<pk>\d+)$', views.libraries_edit, name='libraries-edit'),
    url(r'^addlibraries$', views.addlibraries, name='addlibraries'),
    url(r'^editlibraries/(?P<id>\d+)$', views.editlibraries, name='editlibraries'),
]
