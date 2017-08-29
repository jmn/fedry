from django.core.management.base import BaseCommand #, CommandError
from fd.models import FeedSource, FeedPost
from datetime import datetime, timedelta, timezone
import feedparser
import functools
import time
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc

def timetuple_to_datetime(t):
    return datetime(*t[:6])

@timeit
def update_feeds(FeedSource, FeedPost):
    num_posts_created = 0

    for feed in FeedSource.objects.all():
        print(feed.title)

        if feed.date_parsed and feed.date_parsed > datetime.now(timezone.utc) - timedelta(minutes=1):
            print("Not updating %s because it was updated recently." % feed.title)
            continue
        else:
            feed.date_parsed = datetime.now(timezone.utc)
            feed.save()
            
        fis = feedparser.parse(feed.url, modified=feed.date_modified, etag=feed.etag)

        if fis.status == '304': # feed has not changed
            print("Feed '%s' unchanged according to ETag or date-modified: not updating." % feed.title)
            continue

        else:
            mod = False
            if fis.has_key('etag'):
                feed.etag = fis.etag
                feed.save()
                mod = True                
            if fis.has_key('updated_parsed'):
                feed.date_modified = timetuple_to_datetime(fis.updated_parsed)
                mod = True
            if mod:
                feed.save()

        insert_posts(feed, fis.entries)
        print("inserting posts")

    return num_posts_created

# Preprocessing. Convert relative URLs to absolute.
def convert_absolute_img_urls(content, base_url='http://example.com'):
    soup = BeautifulSoup(content, 'html.parser')

    for link in soup.find_all("img", src=True):
        absolute_url = urljoin(base_url, link["src"]) 
        link["src"] = absolute_url

    for link in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, link["href"]) # TODO: Don't touch links starting with "#" (internal links.)
        link["href"] = absolute_url

    return soup.prettify()

def insert_posts(feed, entries):
    num_created = 0
    for f in entries:
        if f.has_key('author'):
            author = f.author
        else:
            author = "Unknown"

        if f.has_key('published_parsed'):
            pub_date = datetime(*f.published_parsed[:6]) #FIXME: Need a better time conversion.
        else:
            pub_date = timetuple_to_datetime(f.updated_parsed) #FIXME: Need a better time conversion.                pub_date = 

        # clean up content
        base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(f.link))
        content = convert_absolute_img_urls(f.content[0].value, base_url)

        (fp, created) = FeedPost.objects.get_or_create(
            feed=feed,
            url=f.link,
            defaults={'feed': feed,
                      'title': f.title,
                      'url': f.link,
                      'author': author,
                      'content': content,
                      'date_acquired': datetime.now(),
                      'date_published': pub_date}
        )

        if created:
            num_created += 1    
    return num_created

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
