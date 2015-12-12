from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import  User,Group
from django.template import RequestContext
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy 



def index_view(request):

    Responsable=Group.objects.filter(name="Planificador")
    Estudiante=Group.objects.filter(name="Estudiante")
    Profesor=Group.objects.filter(name="Profesor")
    if str(Responsable) == "[]" and str(Estudiante)=="[]" and str(Profesor)=="[]":
        g=Group()
        for i in range(4):
            if i == 1:
                g=Group()
                g.name="Responsable"
                g.save()
            if i == 2:
                g=Group()
                g.name="Estudiante"
                g.save()
            if i == 3:
                g=Group()
                g.name="Profesor"
                g.save()

        grupos = Group.objects.filter(id=1)
        user=User.objects.get(id=1)
        user.groups=grupos
        user.save()
        return HttpResponseRedirect('administracion/login/')
    if request.user.is_authenticated():
        USUARIO=request.user.username
                  
        return render_to_response('base.html',{'users':USUARIO},RequestContext(request))
    else:
        return HttpResponseRedirect('administracion/login/')