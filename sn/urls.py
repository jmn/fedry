from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^write/$', views.write, name='write'),
]
