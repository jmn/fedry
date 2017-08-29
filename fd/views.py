from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from fd.models import FeedPost, FeedSource
from itertools import chain
from django.contrib.auth.models import User

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

def tags_overview(request, username):
    user = get_object_or_404(User, username=username)
#    users_fs = FeedSource.objects.filter(user=user)
    all_users_tags = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=user).distinct()

    users_tags = {}
    for t in all_users_tags:
        sources = FeedSource.objects.filter(tags=t)
        posts = []
        for f in sources:                                        # for each f in fs, get all objects which has post.feed = f
            posts.append(FeedPost.objects.filter(feed=f))
        result = list(chain(*posts)) # extract the querysets into a list using itertools.chain 
        users_tags[t] = result

    context = {'users_tags': users_tags}
    return render(request, 'fd/tags_overview.html', context)
