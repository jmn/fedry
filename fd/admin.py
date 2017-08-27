from django.contrib import admin

from fd.models import FeedSource, FeedPost

# Register your models here.
admin.site.register(FeedSource)
admin.site.register(FeedPost)
