# post
from graphene_django import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from django.contrib.auth.models import User
from fd.models import FeedPost, FeedSource
from django.db import models
from django.db.models import F, Q
import tagulous.models
import graphene
from graphql_relay.node.node import from_global_id
import graphql_jwt

class PostType(DjangoObjectType):

    class Meta:
        model = FeedPost
        interfaces = (graphene.relay.Node,)
        filter_fields = ['feed']

class Tags(graphene.ObjectType):
    tag_list = graphene.List(graphene.String)

    def resolve_tag_list(self, info):
        username = info.context.args.get('username')
        u = User.objects.get(username=username)
        f = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=u).distinct()
        tags = [tag.name for tag in f.all()]
        return tags

class AddFeed(graphene.Mutation):
    class Arguments:
        url = graphene.String()
        name = graphene.String()
        
class Query(graphene.ObjectType):
    current_user = graphene.Field(UserType)
    post = graphene.Node.Field(PostType, username = graphene.String())
    all_posts = DjangoFilterConnectionField(PostType, id=graphene.ID(), username=graphene.String(required=True), q=graphene.String(), tags=graphene.String())
    all_tags = graphene.List(Tags, username=graphene.String())

    def resolve_current_user(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user
    

    # This is weird. Passing args with graphene:
    # https://github.com/graphql-python/graphene/issues/378#issuecomment-352206929

    def resolve_all_tags(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
#        return user

        info.context.args = dict(username=kwargs.get("username"))
        return [Tags()] 

    # https://stackoverflow.com/a/39774434/41829
    def resolve_all_posts(self, info, **kwargs):
        username = kwargs.get('username')
        u = User.objects.get(username=username)
        searchterm = kwargs.get('q')
        tags = kwargs.get('tags')
        id = kwargs.get('id')
        if id:
            rid = from_global_id(id)[1]
            return (FeedPost.objects.all().filter(pk=rid))

        if tags:
            users_sources = FeedSource.objects.filter(user=u, tags=tags, show_on_frontpage=True)
        else:
            users_sources = FeedSource.objects.filter(user=u, show_on_frontpage=True)
        if searchterm:
            queryset = FeedPost.objects.filter(feed__feedsource__in=users_sources).filter(Q(title__icontains=searchterm) | Q(content__icontains=searchterm)).annotate(source_title=F('feed__feedsource__title'))
        else: 
            queryset = FeedPost.objects.filter(feed__feedsource__in=users_sources).annotate(
                source_title=F('feed__feedsource__title'))
        return queryset
        
class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
