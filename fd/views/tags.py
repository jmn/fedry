from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

def posts_by_tags(request, tag): # FIXME: Convert to taglist
    fs = FeedSource.objects.filter(tags=tag)

    posts = []
    for f in fs:                                        # for each f in fs, get all objects which has post.feed = f
        posts.append(FeedPost.objects.order_by('-date_published').filter(feed=f))

    result = list(chain(*posts)) # extract the querysets into a list using itertools.chain 
    tag_list = FeedSource.tags.tag_model.objects.all()     # all tags
    return render(request, 'fd/topics.html', {'object_list': result, 'tag_list': tag_list})

def tags_overview(request, username):
    user = get_object_or_404(User, username=username)
    all_users_tags = FeedSource.tags.tag_model.objects.filter_or_initial(feedsource__user=user).distinct()

    users_tags = {}
    for t in all_users_tags:
        sources = FeedSource.objects.filter(tags=t)
        posts = []
        for f in sources:                                        # for each f in fs, get all objects which has post.feed = f
            posts.append(FeedPost.objects.order_by('-date_published').filter(feed=f)) 
        result = list(chain(*posts)) # extract the querysets into a list using itertools.chain  #FIXME: Order ALL
        users_tags[t] = result

    context = {'users_tags': users_tags}
    return render(request, 'fd/tags_overview.html', context)

def user_tags_overview(request, username="", tags=""):
    user = get_object_or_404(User, username=username)
    tags = tags.split(",")
   
    users_tags = {}
    for t in tags:
        sources = get_list_or_404(FeedSource, tags=t)

        posts = []
        for f in sources:                                        # for each f in fs, get all objects which has post.feed = f
            posts.append(FeedPost.objects.filter(feed=f))
        result = list(chain(*posts)) # extract the querysets into a list using itertools.chain 

        users_tags[t] = result

    context = {'users_tags': users_tags}
    return render(request, 'fd/tags_overview.html', context)
