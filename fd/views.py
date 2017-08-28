from django.shortcuts import render
from django.views.generic import ListView
from fd.models import FeedPost

class PostList(ListView):
    model = FeedPost
    paginate_by = 3

