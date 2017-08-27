from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone

# Create your views here.
from .forms import PostForm
from .models import Post

def index (request):
    return render(request, 'sn/index.html')

@login_required
def home(request):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    context = {'posts':posts}
    
    return render(request, 'sn/home.html', context)

@login_required
def write(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # TODO: check for add post privgs.
            post.pub_date = timezone.now()
            post.save()
            # TODO: process the data.
            return HttpResponseRedirect('/s/') # FIXME: Use name instead of URL
    else:
        form = PostForm
    
    return render(request, 'sn/write.html', {'form' : form})
