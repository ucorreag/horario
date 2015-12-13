
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

# Create your views here.
def login_required(function):
    def wrapper(*args,**kwargs):
        request = args[0]
        if not request.user.is_authenticated() and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('login'))
        elif request.user.is_authenticated() and not request.user.is_superuser:
            logout(request)
            return HttpResponseRedirect(reverse('login'))
        else:
            return function(*args,**kwargs)
    return wrapper

