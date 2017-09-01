from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView
from fd.models import FeedPost, FeedSource
from itertools import chain
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class SourceCreate(LoginRequiredMixin, CreateView):
    model = FeedSource
    fields = ['title', 'url', 'tags']
    success_url = reverse_lazy('source_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SourceCreate, self).form_valid(form)

class SourceEdit(UpdateView):
    template_name = 'fd/edit_sources.html'
    model = FeedSource
    fields = ['title', 'url', 'tags']
    success_url = reverse_lazy('source_list')

class SourceList(ListView):
    model = FeedSource
    paginate_by = 10
    
    def get_queryset(self):
        return FeedSource.objects.filter(user=self.request.user)

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
        context['tag_list'] = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=self.request.user).distinct()
        context['sources_list'] = FeedSource.objects.filter(user=self.request.user)
        return context

def post_detail(request, post_id):
    # prev_id, next_id as GET Params
    
    post = get_object_or_404(FeedPost, pk=post_id)
    next_post = FeedPost.get_next_by_date_published(post) # FIXME: This is sketchy because of it's not context-aware.
    prev_post = FeedPost.get_previous_by_date_published(post)

    return render(request, 'fd/post_detail.html', {'post': post, 'next_post': next_post,'prev_post': prev_post})

def posts_by_tags(request, tag): # FIXME: Convert to taglist
    fs = FeedSource.objects.filter(tags=tag)

    posts = []
    for f in fs:                                        # for each f in fs, get all objects which has post.feed = f
        posts.append(FeedPost.objects.order_by('date_published').filter(feed=f))

    result = list(chain(*posts)) # extract the querysets into a list using itertools.chain 
    tag_list = FeedSource.tags.tag_model.objects.all()     # all tags
    return render(request, 'fd/topics.html', {'object_list': result, 'tag_list': tag_list})

def tags_overview(request, username):
    user = get_object_or_404(User, username=username)
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

def user_tags_overview(request, username="", tags=""):
    user = get_object_or_404(User, username=username)
    tags = tags.split(",")
   
    users_tags = {}
    for t in tags:
        sources = get_list_or_404(FeedSource, tags=t)

        posts = []
        for f in sources:                                        # for each f in fs, get all objects which has post.feed = f
            posts.append(FeedPost.objects.filter(feed=f))
        result = list(chain(*posts)) # extract the querysets into a list using itertools.chain 
        print(t)
        users_tags[t] = result

    context = {'users_tags': users_tags}
    return render(request, 'fd/tags_overview.html', context)
