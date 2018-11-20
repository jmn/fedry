# post
from graphene_django import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField

from fd.models import FeedPost
import graphene

class Post(DjangoObjectType):
    class Meta:
        model = FeedPost
        interfaces = (graphene.Node,)
        filter_fields = []
        
class Query(graphene.ObjectType):
#    posts = graphene.List(Post)
    posts = DjangoFilterConnectionField(Post)    

    def resolve_posts(self, info, **args):
        return FeedPost.objects.all()

schema = graphene.Schema(query=Query)
