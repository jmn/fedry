from django.conf.urls import url, include

from . import views

# fedry.net/v/username/tagname
# fedry.net/~username/tag1,tag2
# e.g. I read Haskell at fedry.net/~jmn/haskell

urlpatterns = [
    url(r'^(?P<tag>[\w-]+)$', views.posts_by_tags),
    url(r'^topics/$', views.PostIndexView.as_view()), 
    url(r'^new/$', views.PostList.as_view()),
]
