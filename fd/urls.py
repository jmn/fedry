from django.conf.urls import url, include

from . import views

# fedry.net/v/username/tagname
# fedry.net/~username/tag1,tag2
# e.g. I read Haskell at fedry.net/~jmn/haskell

urlpatterns = [
    url(r'^$', views.PostIndexView.as_view()),
#    url(r'^$', views.index),    
#    url(r'^(?P<tag>[\w-]+)$', views.posts_by_tags, name='tags'),
    url(r'^view/(?P<post_id>[\w-]+)$', views.post_detail, name='post_detail'),
    url(r'^t/(?P<username>[\w-]+)$', views.tags_overview, name='tags_overview'),
#    url(r'^t/(?P<username>[\w-]+)/(?P<tags>\w+)$', views.user_tags_overview, name='tags'),
    url(r'^t/(?P<username>[\w-]+)/(?P<tags>\w+)$', views.PostIndexView.as_view(), name='tags'),    
    url(r'^topics/$', views.PostIndexView.as_view(), name='topics_view'),
    url(r'^new/$', views.PostList.as_view(), name='detailed_list'),
    url(r'^sourcelist/$', views.SourceList.as_view(), name='source_list'),
    url(r'^edit/(?P<pk>[\w-]+)$', views.SourceEdit.as_view(), name='source_edit'),
    url(r'^add/$', views.SourceCreate.as_view(), name='source_create'),
]
