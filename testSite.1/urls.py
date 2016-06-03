"""testSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
import cab.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('dashboard.urls')),
    url(r'^profile/', include('cab.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^statistic/', include('statistic.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},
                           name='auth_login'),
    url(r'^logout/$', cab.views.cab_logout, name='auth_logout'),
    url(r'^register/$', cab.views.register, name='auth_register'),
    url(r'^about/$', include('about.urls'))
]
