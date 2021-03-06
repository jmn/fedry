from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from fd.models import FeedSource, FeedPost
from django.urls import reverse_lazy
from fd.forms import *
from fd.views.posts import PaginatedProtectedListView # FIXME: Move this class
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DeleteView
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

class PermissionMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied()
        else:
            return obj
        
class SourceDelete(PermissionMixin, DeleteView):
    model = FeedSource
    success_url = reverse_lazy('source_list')

class SourceCreate(LoginRequiredMixin, CreateView):
    model = FeedSource
    success_url = reverse_lazy('source_list')
    form_class = SourceCreateForm
    
    def form_valid(self, form):
        url = form.cleaned_data['url']
        # see if this url already exists in Feeds, if not create it
        feed = Feed.objects.get_or_create(url=url)[0]
        form.instance.user = self.request.user
        form.instance.feed = feed
        response = super(SourceCreate, self).form_valid(form)
        return response

class SourceEdit(UpdateView):
    template_name = 'fd/edit_sources.html'
    model = FeedSource
    fields = ['title', 'tags', 'show_on_frontpage']
    success_url = reverse_lazy('source_list')

    def get_permission_required(self):
        return

    # Restrict to editing sources belonging to this user.
    def get_queryset(self):
        base_qs = super(SourceEdit, self).get_queryset()
        return base_qs.filter(user=self.request.user)

class SourceList(PaginatedProtectedListView):
    model = FeedSource
    paginate_by = 10
    
    def get_queryset(self):
        return FeedSource.objects.filter(user=self.request.user)

