from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class FeedSource(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    date_parsed = models.DateTimeField(blank=True, null=True)
    etag = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title
    
class FeedPost(models.Model):
    feed = models.ForeignKey(FeedSource)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, primary_key=True)
    author = models.CharField(max_length=200)
    content = models.TextField()
    date_acquired = models.DateTimeField()
    date_published = models.DateTimeField()

    class Meta:
        ordering = ["date_acquired"]
    # def __str__(self):
    #     return self.
