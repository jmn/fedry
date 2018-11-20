# post
from graphene_django import DjangoObjectType
from fd.models import FeedPost
import graphene

class Post(DjangoObjectType):
    class Meta:
        model = FeedPost

class Query(graphene.ObjectType):
    posts = graphene.List(Post)

    def resolve_posts(self, info):
        return FeedPost.objects.all()

schema = graphene.Schema(query=Query)
