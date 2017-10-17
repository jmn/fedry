from fd.models import FeedPost
from fd.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def posts_list(request):
    posts = FeedPost.objects.all()[:10]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
