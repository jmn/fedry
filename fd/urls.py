from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^topics/$', views.PostIndexView.as_view()), 
    url(r'^new/$', views.PostList.as_view()),
]
