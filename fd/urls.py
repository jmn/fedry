from django.conf.urls import url, include

from . import views

# fedry.net/v/username/tagname
# fedry.net/~username/tag1,tag2
# e.g. I read Haskell at fedry.net/~jmn/haskell

urlpatterns = [
    url(r'^$', views.PostIndexView.as_view()),
#    url(r'^$', views.index),    
    url(r'^(?P<tag>[\w-]+)$', views.posts_by_tags, name='tags'),
    url(r'^view/(?P<post_id>[\w-]+)$', views.post_detail, name='post_detail'),
    url(r'^t/(?P<username>[\w-]+)$', views.tags_overview, name='tags_overview'),
    url(r'^topics/$', views.PostIndexView.as_view(), name='topics_view'),
    url(r'^new/$', views.PostList.as_view(), name='detailed_list'),
]
