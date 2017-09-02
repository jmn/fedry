from django.db.models.signals import post_save
from django.dispatch import receiver
from fd.models import FeedSource
from fd.services import get_initial_posts
import django_rq

@receiver(post_save, sender=FeedSource)
def fetch_initial_posts(sender, instance, created, **kwargs):
    queue = django_rq.get_queue('high')
    queue.enqueue(get_initial_posts, feedsource_pk=instance.pk)
