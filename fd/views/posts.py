from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView
from fd.models import FeedPost, FeedSource

from itertools import chain
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required


class PaginatedListView(ListView):
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})
        return context
    

class PostList(PaginatedListView):
    model = FeedPost
    paginate_by = 3

class PostIndexView(PaginatedListView):
    template_name = 'fd/topics.html'
    model = FeedPost
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostIndexView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        users_sources = FeedSource.objects.filter(user=self.request.user)
        user_source_pks = users_sources.values_list('id', flat=True)

        if 'tags' in self.kwargs:
            tags = self.kwargs['tags']
        
            tag_id = FeedSource.tags.tag_model.objects.filter(slug=tags)[0]
            return FeedPost.objects.filter(feed__in=user_source_pks, feed__tags=tag_id)

        posts = FeedPost.objects.filter(feed_sources__in=user_source_pks)
        for fs in users_sources: # FIXME: This must be very slow
            for p in posts:
                if p.feed == fs.feed:
                    p.source_title = fs.title
        return posts

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostIndexView, self).get_context_data(**kwargs)

        context['tag_list'] = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=self.request.user).distinct()
        if 'tags' in self.kwargs:
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user, tags=self.kwargs['tags'])
        else:
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user)
            
        return context

def post_detail(request, post_id):
    # prev_id, next_id as GET Params
    
    post = get_object_or_404(FeedPost, pk=post_id)
    try:
        next_post = FeedPost.get_next_by_date_published(post) # FIXME: This is sketchy because of it's not context-aware.
    except FeedPost.DoesNotExist:
        next_post = ''
        
    try:
        prev_post = FeedPost.get_previous_by_date_published(post)
    except FeedPost.DoesNotExist:
        prev_post = ''
        
    return render(request, 'fd/post_detail.html', {'post': post, 'next_post': next_post,'prev_post': prev_post})
