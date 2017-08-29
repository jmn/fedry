from django.shortcuts import render
from django.views.generic import ListView
from fd.models import FeedPost, FeedSource
from itertools import chain


class PostList(ListView):
    model = FeedPost
    paginate_by = 3

class PostIndexView(ListView):
    template_name = 'fd/topics.html'
    model = FeedPost
    paginate_by = 10

def posts_by_tags(request, tag): # FIXME: Convert to taglist
    fs = FeedSource.objects.filter(tags=tag)

    posts = []
    for f in fs:                                        # for each f in fs, get all objects which has post.feed = f
        posts.append(FeedPost.objects.filter(feed=f))

    result = list(chain(*posts)) # extract the querysets into a list using itertools.chain 
    tag_list = FeedSource.tags.tag_model.objects.all()     # all tags
    return render(request, 'fd/topics.html', {'object_list': result, 'tag_list': tag_list})
