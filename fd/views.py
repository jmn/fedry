from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from fd.models import FeedPost, FeedSource
from itertools import chain
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

class PostList(ListView):
    model = FeedPost
    paginate_by = 3

class PostIndexView(ListView):
    template_name = 'fd/topics.html'
    model = FeedPost
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostIndexView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return FeedPost.objects.filter(feed__user=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tag_list'] = FeedSource.tags.tag_model.objects.all()
        context['sources_list'] = FeedSource.objects.filter(user=self.request.user)
        return context

def post_detail(request, post_id):
    post = get_object_or_404(FeedPost, pk=post_id)
    return render(request, 'fd/post_detail.html', {'post': post})

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
