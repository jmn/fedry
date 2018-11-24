# post
from graphene_django import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from django.contrib.auth.models import User
from fd.models import FeedPost, FeedSource
from django.db import models
from django.db.models import F
import graphene

class PostType(DjangoObjectType):
    username = graphene.Field(graphene.String, required=True)

    class Meta:
        model = FeedPost
        interfaces = (graphene.relay.Node,)
        filter_fields = ['feed']
        
class Query(graphene.ObjectType):
    post = graphene.Node.Field(PostType, username = graphene.String())
    all_posts = DjangoFilterConnectionField(PostType, username=graphene.String(required=True))
    reverse = graphene.String(word=graphene.String())

    def resolve_reverse(self, info, word):
        return word[::-1]

    # https://stackoverflow.com/a/39774434/41829
    def resolve_all_posts(self, info, **kwargs):
        username = kwargs.get('username')
        u = User.objects.get(username=username) 
        users_sources = FeedSource.objects.filter(user=u, show_on_frontpage=True)
        return FeedPost.objects.filter(feed__feedsource__in=users_sources).annotate(
            source_title=F('feed__feedsource__title')
        )
        
schema = graphene.Schema(query=Query)
