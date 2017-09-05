from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone

# Create your views here.
def index (request):
    return render(request, 'sn/index.html')

