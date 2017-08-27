from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from .forms import PostForm

def index (request):
    context = {}
    return render(request, 'sn/index.html', context)

@login_required
def home(request):
    return render(request, 'sn/home.html')

@login_required
def write(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            # TODO: process the data.
            return HttpResponseRedirect('/s/') # FIXME: Use name instead of URL
    else:
        form = PostForm
    
    return render(request, 'sn/write.html', {'form' : form})
