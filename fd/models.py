from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tagulous.models import TagField
# Create your models here.

class Feed(models.Model):
    url = models.URLField(max_length=200)
    etag = models.CharField(max_length=200, blank=True, null=True)
    date_parsed = models.DateTimeField(blank=True, null=True)
    date_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.url

class FeedSource(models.Model):
    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=200)
    show_on_frontpage = models.BooleanField(default=True)
    tags = TagField()

    def __str__(self):
        return self.title

    @property
    def posting_avg(self):
        return 47

    class Meta:
        ordering = ["title"]
        unique_together = (("user", "feed"))
        
class FeedPost(models.Model):
<<<<<<< HEAD
    feed = models.ForeignKey(FeedSource)
=======
    feed = models.ForeignKey(Feed)
    feed_sources = models.ManyToManyField(FeedSource)
>>>>>>> ab0ee2ffe39636057c4dbca23b54f9b457fbebe4
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    date_acquired = models.DateTimeField()
    date_published = models.DateTimeField()

    class Meta:
        ordering = ["-date_published"]
        unique_together = (("feed", "url")) # FIXME: quick hack.
    # def __str__(self): # FIXME: is it safe to use self.title?
    #     return self.
