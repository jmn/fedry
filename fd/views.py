from django.shortcuts import render
from django.views.generic import ListView
from fd.models import FeedPost

class PostList(ListView):
    model = FeedPost
    paginate_by = 3

class PostIndexView(ListView):
    template_name = 'fd/topics.html'
    model = FeedPost
    paginate_by = 10
