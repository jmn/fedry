from django.db.models.signals import post_save
from django.dispatch import receiver
from fd.models import FeedSource
from fd.services import get_initial_posts
import django_rq
import logging

@receiver(post_save, sender=FeedSource)
def fetch_initial_posts(sender, instance, created, **kwargs):
    logger = logging.getLogger(__name__)
    logger.debug('NEW SAVE!')
    django_rq.enqueue(get_initial_posts, feedsource_pk=instance.pk)
#    get_initial_posts(feedsource_pk=instance.pk)
    print("NEW Save! :-)")
