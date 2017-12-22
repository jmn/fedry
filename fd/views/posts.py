from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView
from fd.models import FeedPost, FeedSource

from itertools import chain
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.utils.decorators import method_decorator


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

class PaginatedProtectedListView(PaginatedListView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaginatedProtectedListView, self).dispatch(*args, **kwargs)
    
# Detailed list view
class PostList(PaginatedListView):
    model = FeedPost
    paginate_by = 3

    def get_queryset(self):
        if 'tags' in self.kwargs:
            tags = self.kwargs['tags']
            users_sources = FeedSource.objects.filter(user=self.request.user, tags=tags)
            
        else:
            users_sources = FeedSource.objects.filter(user=self.request.user, show_on_frontpage=True)

        return FeedPost.objects.filter(feed__feedsource__in=users_sources).annotate(
            source_title=F('feed__feedsource__title')
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostList, self).get_context_data(**kwargs)
        context['tag_list'] = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=self.request.user).distinct()

        if 'tags' in self.kwargs:
            context['tag_view'] = self.kwargs['tags']
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user, tags=self.kwargs['tags'])
        else:
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user, show_on_frontpage=True)
            
        return context

# overview
from django.db.models import Value, CharField, Func
from django.db.models.expressions import  RawSQL
from next_prev import next_in_order, prev_in_order

class LagLead(Func):
    function = 'LAG'
    template = '%(function)s(id) OVER (ORDER BY id)'

class PostIndexView(LoginRequiredMixin, PaginatedListView):
    login_url = '/introduction/'
    template_name = 'fd/topics.html'
    model = FeedPost
    paginate_by = 10

    def get_queryset(self):
        if 'tags' in self.kwargs:
            tags = self.kwargs['tags']
            users_sources = FeedSource.objects.filter(user=self.request.user, tags=tags)  
          
        else:
            users_sources = FeedSource.objects.filter(user=self.request.user, show_on_frontpage=True)
        return FeedPost.objects.filter(feed__feedsource__in=users_sources).annotate(source_title=F('feed__feedsource__title'))

#        return FeedPost.objects.annotate(next=RawSQL("lead(id) OVER (ORDER BY id)", []))
       # return FeedPost.objects.filter(feed__feedsource__in=users_sources).extra(select={'next': 'LEAD(fd_feedpost.id) OVER (ORDER BY fd_feedpost.id)'}).extra(select={'prev': 'LAG(fd_feedpost.id) OVER (ORDER BY fd_feedpost.id)'}).annotate(source_title=F('feed__feedsource__title'))
#            "lag(fd_feedpost.id) over (order by fd_feedpost.id)"
#            , []
#        )).annotate(source_title=F('feed__feedsource__title'))
    #        return FeedPost.objects.filter(feed__feedsource__in=users_sources).annotate(next=RawSQL("select *, lag(id) over (order by id) from fd_feedpost", ()))
#        )
# .annotate(            source_title=F('feed__feedsource__title'))
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostIndexView, self).get_context_data(**kwargs)

        context['tag_list'] = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=self.request.user).distinct()
        if 'tags' in self.kwargs:
            context['tag_view'] = self.kwargs['tags']
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user, tags=self.kwargs['tags'])
        else:
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user, show_on_frontpage=True)
            
        return context

    def dispatch(self, *args, **kwargs):
        return super(PostIndexView, self).dispatch(*args, **kwargs)

def post_detail(request, post_id):
    # prev_id, next_id as GET Params
    
    post = get_object_or_404(FeedPost, pk=post_id)
    users_sources = FeedSource.objects.filter(user=request.user, show_on_frontpage=True)
    try:
        next_post = next_in_order(post, FeedPost.objects.filter(feed__feedsource__in=users_sources))
    except FeedPost.DoesNotExist:
        next_post = ''
        
    try:
        prev_post = prev_in_order(post, FeedPost.objects.filter(feed__feedsource__in=users_sources))
    except FeedPost.DoesNotExist:
        prev_post = ''
        
    return render(request, 'fd/post_detail.html', {'post': post, 'next_post': next_post,'prev_post': prev_post})
