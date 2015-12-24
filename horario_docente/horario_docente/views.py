from django.http import  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import  User,Group
from django.template import RequestContext
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy 
from apps.horario.models import *

def index_view(request):
    if str(Semestre.objects.all()) == "[]":
               
        ps=Semestre(nombre='primero')
        ps.save()
        sg=Semestre(nombre='segundo')
        sg.save()
    
        semestre=Semestre.objects.all()
        for sem in semestre:
            pr=Año(nombre='primero', id_semestre=sem)
            pr.save()
            seg=Año(nombre='segundo',id_semestre=sem)
            seg.save()
            ter=Año(nombre='tercero', id_semestre=sem)
            ter.save()
            cuar=Año(nombre='cuarto', id_semestre=sem)
            cuar.save()
            quin=Año(nombre='quinto', id_semestre=sem)
            quin.save()
            
        categ1=Categoria(nombre="pregrado")
        categ2=Categoria(nombre="postgrado")
        categ1.save()
        categ2.save()
        
         
        conf=Tipo(nombre="conferencia")
        conf.save()
        cp=Tipo(nombre="clase práctica")
        cp.save()
        lab=Tipo(nombre="laboratorio")
        lab.save()
        sem=Tipo(nombre="seminario")
        sem.save()
        tl=Tipo(nombre="prueba parcial")
        tl.save()
        tl=Tipo(nombre="proyecto de curso")
        tl.save()
        cnp=Tipo(nombre="otras actividades")
        cnp.save()
        tl=Tipo(nombre="taller")
        tl.save()
        
        
        return HttpResponseRedirect(reverse_lazy('home'))   
    
    
   # Planificador=Group.objects.filter(name="Planificador")
   # Profesor=Group.objects.filter(name="Profesor")
   # if str(Planificador) == "[]" and str(Profesor)=="[]":
   #     g=Group()
   #     for i in range(4):
   #         if i == 1:
   #             g=Group()
   #             g.name="Planificador"
   #             g.save()
   #         if i == 2:
   #             g=Group()
   #             g.name="Profesor"
   #             g.save()
   #         
   #     grupos = Group.objects.filter(id=1)
   #     user=User.objects.get(id=1)
   #     user.groups=grupos
   #     user.save()
    facultad=Facultad.objects.all()
    semestre=Semestre.objects.all()
    carrerasa=CarreraAño.objects.all()
    carreras=Carrera.objects.all()
    facultadcategoria=FacultadCategoria.objects.all()
    usuarios=User.objects.all() 
    semana=Semana.objects.all()
    aux={
        'facultad': facultad,
        'semestre': semestre,
        'carrerasaño': carrerasa,
        'carreras':carreras,
        'facultadcategoria':facultadcategoria,
        'usuarios':usuarios,
        'semana':semana,
    }           
    return render_to_response('base.html',aux,RequestContext(request))