from fd.models import FeedSource, FeedPost
import feedparser
from datetime import datetime, timedelta, timezone
import feedparser
import functools
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# defines functions shared by signals and commands
# among other things.
def update_from_all_feeds():

    for feedsource in FeedSource.objects.all():
        feed = feedsource.feed

        if feed.date_parsed and feed.date_parsed == datetime.now(timezone.utc) - timedelta(minutes=1): #FIXME: Flip < to >
#            print("Not updating %s because it was updated recently." % feed.title)
            continue
        else:
            feed.date_parsed = datetime.now(timezone.utc)
            feed.save()
            
        parsed = feedparser.parse(feed.url) #, modified=feed.date_modified, etag=feed.etag) # FIXME Re-enable this DEBUG

        if parsed.status == '304': # feed has not changed
            print("Feed '%s' unchanged according to ETag or date-modified: not updating." % feed.title)
            continue

        else:
            mod = False
            if parsed.has_key('etag'):
                feed.etag = parsed.etag
                feed.save()
                mod = True                
            if parsed.has_key('updated_parsed'):
                feed.date_modified = timetuple_to_datetime(parsed.updated_parsed)
                mod = True
            if mod:
                feed.save()

        insert_posts(feedsource, parsed.entries)

def get_initial_posts(feedsource_pk):
    f = FeedSource.objects.get(pk=feedsource_pk)
    parsed = feedparser.parse(f.feed.url)
    insert_posts(f, parsed.entries)

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


def insert_posts(feedsource, entries):
    print( "inserting")
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
        if f.has_key('content'):
            content = f.content[0].value
        else:
            content = f.summary
        content = convert_absolute_img_urls(content, base_url)

        (fp, created) = FeedPost.objects.get_or_create(
            feed=feedsource.feed,
            url=f.link[:180],
            defaults={'feed': feedsource.feed,
                      'title': f.title[:180],
                      'url': f.link[:180],
                      'author': author[:180],
                      'content': content,
                      'date_acquired': datetime.now(),
                      'date_published': pub_date}
        )
        fp.feed_sources.add(feedsource)
        fp.save()

        if created:
            num_created += 1    
    return num_created
