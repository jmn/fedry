from fd.views.posts import PaginatedListView
from fd.models import FeedPost, FeedSource
from django.db.models import F

class PostSearch(PaginatedListView):
    model = FeedPost
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q')
        users_sources = FeedSource.objects.filter(user=self.request.user)
                
        return FeedPost.objects.filter(feed__feedsource__in=users_sources, content__search=query).annotate(
            source_title=F('feed__feedsource__title')
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostSearch, self).get_context_data(**kwargs)
        context['tag_list'] = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=self.request.user).distinct()

        if 'tags' in self.kwargs:
            context['tag_view'] = self.kwargs['tags']
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user, tags=self.kwargs['tags'])
        else:
            context['sources_list'] = FeedSource.objects.filter(user=self.request.user)
            
        return context
