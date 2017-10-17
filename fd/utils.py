from django.shortcuts import HttpResponseRedirect

class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated():
            return HttpResponseRedirect('landing')
        return response
