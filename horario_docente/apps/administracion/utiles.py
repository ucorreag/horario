
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


# Create your views here.
def login_required(function):
    def wrapper(*args):
        request = args[0]
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login/'))
        else:
            return function(*args)
    return wrapper

