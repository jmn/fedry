from django.conf.urls import url, include

from . import views
from fd.views import *
from fd.views.posts import *
from fd.views.tags import *
from fd.views.sources import *
from fd.views.search import *
from fd.views.profile import *
from fd.views.api.posts import *
from django.views.generic import TemplateView


# fedry.net/v/username/tagname
# fedry.net/~username/tag1,tag2
# e.g. I read Haskell at fedry.net/~jmn/haskell

urlpatterns = [
    url(r'^$', PostIndexView.as_view(), name='home'),
    url(r'^introduction/$', TemplateView.as_view(template_name='fd/landing.html'), name='landing'),    
    url(r'^view/(?P<username>[\w-])/(?P<tags>\w-)/(?P<post_id>[\w-]+)$', post_detail, name='post_detail'),
    url(r'^t/(?P<username>[\w-]+)$', tags_overview, name='tags_overview'),
    url(r'^t/(?P<username>[\w-]+)/(?P<tags>\w+)$', PostIndexView.as_view(), name='tags'),
    url(r'^t/(?P<username>[\w-]+)/(?P<tags>\w+)/$', PostList.as_view(), name='tags_detailed'),    
    url(r'^topics/$', PostIndexView.as_view(), name='topics_view'),
    url(r'^new/$', PostList.as_view(), name='detailed_list'),
    url(r'^sourcelist/$', SourceList.as_view(), name='source_list'),
    url(r'^sourcelist/delete/(?P<pk>\d+)/$', SourceDelete.as_view(), name='source_delete'),
    url(r'^edit/(?P<pk>[\w-]+)$', SourceEdit.as_view(), name='source_edit'),
    url(r'^add/$', SourceCreate.as_view(), name='source_create'),
    url(r'^search/$', PostSearch.as_view(), name='search'),
    url(r'^profile/$', get_user_profile, name='profile'),
    url(r'^subscribe/$', subscribe, name='subscribe'),
    url(r'^api/v1/posts', posts_list),
    url(r'^signup/$', signup, name='signup'),
]
