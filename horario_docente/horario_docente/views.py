from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import  User,Group
from django.template import RequestContext
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy 




def index_view(request):

    Planificador=Group.objects.filter(name="Planificador")
    Profesor=Group.objects.filter(name="Profesor")
    if str(Planificador) == "[]" and str(Profesor)=="[]":
        g=Group()
        for i in range(4):
            if i == 1:
                g=Group()
                g.name="Planificador"
                g.save()
            if i == 2:
                g=Group()
                g.name="Profesor"
                g.save()
            
        grupos = Group.objects.filter(id=1)
        user=User.objects.get(id=1)
        user.groups=grupos
        user.save()
        return HttpResponseRedirect(reverse_lazy('home'))
    if request.user.is_authenticated():
        USUARIO=request.user.username
                  
        return render_to_response('base.html',{'users':USUARIO},RequestContext(request))
    else:
        return render_to_response('base.html',RequestContext(request))