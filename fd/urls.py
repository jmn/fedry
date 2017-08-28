from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^new/$', views.PostList.as_view()), 
]
