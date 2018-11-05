from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

# Create your views here.

from django.contrib.auth import login

#from social_django.utils import psa

# Define an URL entry to point to this view, call it passing the
# access_token parameter like ?access_token=<token>. The URL entry must
# contain the backend, like this:
#
#   url(r'^register-by-token/(?P<backend>[^/]+)/$',
#       'register_by_access_token')

# @psa('social:complete')
# def register_by_access_token(request, backend):
#     # This view expects an access_token GET parameter, if it's needed,
#     # request.backend and request.strategy will be loaded with the current
#     # backend and strategy.
#     token = request.GET.get('access_token')
#     user = request.backend.do_auth(token)
#     if user:
#         login(request, user)
#         return 'OK'
#     else:
#         return 'ERROR'
