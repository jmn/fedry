from django.core.management.base import BaseCommand #, CommandError
from fd.models import FeedSource, FeedPost
from datetime import datetime
import feedparser

def update_feeds(FeedSource, FeedPost):
    num_posts_created = 0

    for feed in FeedSource.objects.all():
        print(feed.title)
        fis = feedparser.parse(feed.url)
        for f in fis.entries:
            if f.has_key('author'):
                author = f.author
            else:
                author = "Unknown"

            if f.has_key('published_parsed'):
                pub_date = datetime(*f.published_parsed[:6]) #FIXME: Need a better time conversion.
            else:
                pub_date = datetime(*f.updated_parsed[:6]) #FIXME: Need a better time conversion.                pub_date = 

            (fp, created) = FeedPost.objects.get_or_create(
                feed=feed,
                url=f.link,
                defaults={'feed': feed,
                          'title': f.title,
                          'url': f.link,
                          'author': author,
                          'content': f.summary,
                          'date_acquired': datetime.now(),
                          'date_published': pub_date}
            )

            if created:
                num_posts_created += 1
    return num_posts_created



class Command(BaseCommand):
    help = 'Fetches FeedPosts'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        num_posts_updated = update_feeds(FeedSource, FeedPost)
#        num_feeds_updated = 3 # FIXME
        self.stdout.write(self.style.SUCCESS('Successfully updated %s feeds.'  % num_posts_updated))
