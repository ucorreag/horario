from gettext import gettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import  User,Group
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from apps.horario.models import *
from datetime import *
from django.core.serializers import serialize
import json


from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from .utiles import login_required

#Se han hecho cambios en este m'etodo respecto al oriiginal
def login(request):   
    next =  '/'
    context_dict = {
        'page_title': _('Entrar'),
        }

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            django_login(request, user)
            User.objects.get(username=username)
            return HttpResponseRedirect(next)
        else:
            context_dict['error'] = _('Usuario o contraseña incorrectos')
            
    return render_to_response('login.html', context_dict, RequestContext(request))



@login_required
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('home'))
#Detalles de Usuarios

#Crear Usuarios
#id facultad_categoria
def crear_carrera(request, id):
    if request.POST:
        facultcat=FacultadCategoria.objects.get(id=id)
        nombre=request.POST['nombre']
        cantidad_años=int(request.POST['año'])
        try:
            carrera=Carrera.objects.get(
                nombre=nombre,
                cantidad_años=cantidad_años,
                id_facultad_categoria=facultcat,            
            )
        except ObjectDoesNotExist:            
            carrera=Carrera(
                nombre=nombre,
                cantidad_años=cantidad_años,
                id_facultad_categoria=facultcat,            
            )  
            carrera.save()
        
            semestres=Semestre.objects.all()
            semestre1 = Año.objects.filter(id_semestre=semestres[0].id)
            semestre2 = Año.objects.filter(id_semestre=semestres[1].id)
            conta=0
            for an in semestre1:
                if conta<cantidad_años:
                    m=CarreraAño(id_carrera=carrera, id_año=an)
                    m.save()
                    conta+=1
                    
            conta=0       
            for an in semestre2:
                if conta<cantidad_años:
                    m=CarreraAño(id_carrera=carrera, id_año=an)
                    m.save()
                    conta+=1 
            
        actual = request.META.get('HTTP_REFERER', None) or '/'
        return  HttpResponseRedirect(actual)             





@login_required
def user_create(request):

    context = {
        'p': _('Crear Planificador'),
        
        }
    if request.POST:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

                
        if User.objects.filter(username=username).exists():

            context['error'] = _('El nombre de usuario seleccionado ya existe')
            context['username'] = username
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email
            
        else:
            user= User.objects.create_user(username, email,  password)
            user.first_name= first_name
            user.last_name = last_name
            user.is_staff=True
            user.is_superuser=True
            user.save()

            return HttpResponseRedirect(reverse('lista_usuarios'))

    return render_to_response(
        'Crear_Usuario.html',
        context,
        RequestContext(request)
    )




#Modificar Usuarios
@login_required
def user_update(request,id):
    use=User.objects.get(id=id)
    #IMPLEMNTAR
    
    #users = get_object_or_404(User, pk=id)
    if request.GET:
        username = request.GET['username']
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        password = request.GET['password']
        
        use.first_name= first_name
        use.last_name = last_name
        use.is_staff=True
        use.is_superuser=True
        use.save()
        return HttpResponseRedirect('/administracion/lista_usuarios/')
    
    else:
        return render_to_response(
             'Modificar_Usuario.html',
            {
                'p': _('Actualizar Planificador ' +use.username+''),
                'usuario':use,
                
                },
            RequestContext(request)
        )
           
   
#Eliminar Usuarios
@login_required
def user_delete(request,id):
    actual = request.META.get('HTTP_REFERER', None) or '/'
    e= User.objects.filter(id=id)
    e.delete()
    return HttpResponseRedirect(actual)
    
@login_required   
def profesor_list(request):
    users = Profesor.objects.all()
    if request.POST:
        users=Profesor.objects.filter(nombre=request.POST['nombre'])
       
    
    paginator = Paginator(users, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render_to_response(
         'Lista_profesor.html',
         {             
             'contacts':contacts,
         },
         RequestContext(request)
    )







@login_required   
def user_list(request):
    users = User.objects.all()
    if request.POST:
        users=User.objects.filter(username=request.POST['usuario'])
    
    
    
    paginator = Paginator(users, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render_to_response(
         'Lista_usuario.html',
         {
             
             'contacts':contacts,
         },
         RequestContext(request)
    )

@login_required
def cambiarPassword(request):

    if request.method == "POST":
        password = request.POST['password']
        usuario = request.user
        usuario.password = password
        usuario.set_password(password)
        usuario.save()
        return HttpResponseRedirect(reverse('login'))
        
    else:
        
        return render_to_response('CambiarPassword.html',context_instance = RequestContext(request))
        
 
@login_required
def lista_carreras(request):
    carreras=Carrera.objects.all()
    
    
    return render_to_response('Lista_carreras.html',{'carreras':carreras},context_instance=RequestContext(request))


    
def lista_asignaturas(request, car, an, sem):
       
    carrera=Carrera.objects.get(id=car)
    carann=CarreraAño.objects.filter(id_carrera=carrera.id)
    
   
    anho=Año.objects.get(id=an)
    semestr=Semestre.objects.get(nombre=sem, id_año=anho.id)
    asignaturas=Asignatura.objects.filter(id_carrera=carrera.id, id_semestre=semestr.id)
         
     
    profe=User.objects.filter(groups=2)
        
    if request.POST:
        nombre=request.POST['nombre']
        horas=request.POST['horas']
        profesor=User.objects.get(id=int(request.POST['profesor']))
        val=False
        for asi in asignaturas:
            if asi.nombre == nombre:
                val=True
        if val==False:             
            asig=Asignatura(
                id_profesor=profesor,
                nombre=nombre,
                horas=horas,
                id_semestre=semestr,
                id_carrera=carrera,            
                )
            asig.save()
            tp=Tipo.objects.all()
            for ti in tp:
                astip=AsignaturaTipo(id_asignatura=asig, id_tipo = ti)
                astip.save()  
            
            actual = request.META.get('HTTP_REFERER', None) or '/'
            return  HttpResponseRedirect(actual)
     
  
    sem=Semana.objects.filter(id_carrera=car, id_semestre=semestr.id)
    if sem:
        semana=True
    else:
        semana=False
    
       
    aux={
        'carrerasaños':carann,
        'carrera':carrera,
        'profes':profe,
        'asignaturas':asignaturas,
        'año':anho,
        'semestre':semestr,
        'semana':semana,
        }
    
    
    return render_to_response('Lista_asignaturas.html',aux,RequestContext(request))
    

def crear_semana(request):
    de=request.POST['desde'].split("-")
    d=int(de[0])
    m=int(de[1])
    a=int(de[2])
    
    numero=str(request.POST['numero'])
    año=int(request.POST['año'])
    carrera=int(request.POST['carrera'])
    an=Año.objects.get(id=año)
    car=Carrera.objects.get(id=carrera)
    
    dt=date(d,m,a)
    sem=Semana(
        desde = dt,
        numero=numero,
        id_año=an,
        id_carrera=car,
        )
        
    try:   
        semanas = Semana.objects.get(
            desde = dt,
            numero=numero,
            id_año=an,
            id_carrera=carrera,
            )
    except ObjectDoesNotExist:
        sem.save()
        aux=dt
        dy=dt.day
        mt=dt.month
        yr=dt.year
                       
        smn=sem
        for i in range(75):
            print(date(yr,mt,dy))
            if (i+1)%5 == 0:
               
                
                sm=Semana(
                    desde=date(yr,mt,dy),
                    numero=int((i+1)/5)+1,
                    id_año=an,
                    id_carrera=car,                    
                    )
                sm.save() 
                smn=sm            
                dy+=2
            dy+=1
            if mt==1 and dy>31:
                dy=1
                mt=2
            elif mt==2 and dy>29:
                dy=1
                mt=3
            elif mt==3 and dy>31:
                dy=1
                mt=4
            elif mt==4 and dy>30:
                dy=1
                mt=5
            elif mt==5 and dy>31:
                dy=1
                mt=6
            elif mt==6 and dy>30:
                dy=1
                mt=7
            elif m==7 and dy>31:
                dy=1
                mt=8
            elif mt==8 and dy>31:
                dy=1
                mt=9
            elif mt==9 and dy>30:
                dy=1
                mt=10
            elif mt==10 and dy>31:
                dy=1
                mt=11
            elif mt==11 and dy>30:
                dy=1
                mt=12
            elif mt==12 and dy>31:
                dy=1
                mt=1
                yr+=1 
                
                                    
            fch=date(yr,mt,dy)    
            dias=Dia(fecha=fch, id_semana=smn)
            dias.save()
                    
        
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
     



def eliminar_asignatura(request,id):
    asignatura=Asignatura.objects.get(id=id)
    asignatura.delete()
    
    astp=AsignaturaTipo.objects.filter(id_asignatura=asignatura.id)
    for asp in astp:
        asp.delete()
        
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
     
def eliminar_carrera(request,id):
    carrera=Carrera.objects.get(id=id)
    carrera.delete()
    ca=CarreraAño.objects.filter(id_carrera=id)
    for caa in ca:
        caa.delete()
    
    asig=Asignatura.objects.filter(id_carrera=id)
    for asigna in asig:
        eliminar_asignatura(request,asigna.id)
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)              
        
 
#id año        
def crear_horario(request, id):
    smna=Semana.objects.filter(id_año=id)
    
    x=None
    if smna !=[]:
        x=smna[0]
        for i in smna:
            if x.desde > i.desde:
                x=i             
            
    semanita=x
    
    
    
    dias=[]
    for j in smna:
        dias+=Dia.objects.filter(id_semana=j.id)
    
    turnos=[]   
    for i in dias:
        turnos+=Turno.objects.filter(id_dia=i.id)
    
    isturno=False    
    if turnos !=[]:
        isturno=True
        
    print(isturno)    
    #aux=""
    #lists = [[] for i in range(1,91)]
    #for li in lists:
    #    for i in range(5):
    #        aux+="<td name=\"selda\"><a href=\"\"class=\"btn btn-default\">Añadir</a> </td>"
    #    li.append(aux)
    #    aux=""
    
    asignaturas=Asignatura.objects.filter(id_semestre=id)
    tipos=Tipo.objects.all()   
        
    paginator = Paginator(dias, 5)
    page = request.GET.get('page')
    
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    
    
    facultad=Facultad.objects.all()
    semestre=Semestre.objects.all()
    carrerasa=CarreraAño.objects.all()
    carreras=Carrera.objects.all()
    facultadcategoria=FacultadCategoria.objects.all()
    usuarios=User.objects.all() 
    semana=Semana.objects.all()
      
    
    auxi={
        'lists':contacts,
         'seman':semanita ,
         'turnos':turnos,
         'asignaturas':asignaturas,
         'tipos':tipos,
         'isturno':isturno,
         'facultad': facultad,
         'semestre': semestre,
         'carrerasaño': carrerasa,
         'carreras':carreras,
         'facultadcategoria':facultadcategoria,
         'usuarios':usuarios,
         'semana':semana,
          }
    
    return render_to_response('crear_horario.html',auxi,RequestContext(request)) 
    
    
def crear_turno(request):
    asigna_id=int(request.POST['asignatura'])
    tip_id=int(request.POST['tipp'])
    di=int(request.POST['diass'])
    
    asignatura=Asignatura.objects.get(id=asigna_id)
    tipo=Tipo.objects.get(id=tip_id)
    tn=str(request.POST['turnoo'])
    dia=Dia.objects.get(id=di)
    
        
    at=AsignaturaTipo.objects.get(id_asignatura=asignatura, id_tipo=tipo)
        
    tur=Turno(id_dia=dia,id_asignatura_tipo=at,turno=tn)
    tur.save()
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
    
    
    #crear otros tipos
    
    
    


def crear_facultad(request):
    facultad=request.POST['nombre']
    try:
        facu=Facultad.objects.get(nombre=facultad)
    except ObjectDoesNotExist:
        facu=Facultad(nombre=facultad)
        facu.save()
        
        cate=Categoria.objects.all()
        for caten in cate:
            fc1=FacultadCategoria(id_facultad=facu, id_categoria=caten)
            fc1.save()
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
    
 
 
def is_semana(request):
    if request.is_ajax:
        id_an=int(request.GET['id'])
        sem=Semana.objects.filter(id_año=id_an)
        
        semanas=False
        if sem:
            semanas=True
        
        aux={'semana':semanas}
        
        dato=json.dumps(aux)
        print(semanas)
        return HttpResponse(dato, content_type="application/json")
        
    else:
        raise Http404   
        
     
 
    
def infomacion_preimera_semana(request):
    if request.is_ajax:
               
        id_an=int(request.GET['id'])
        an=Año.objects.get(id=id_an)
        semestre = Semestre.objects.get(id=an.id_semestre.id)
        
        car=CarreraAño.objects.filter(id_año=id_an)
        carA=car[0]        
        carrn=carA.id_carrera.nombre
        carrid=carA.id_carrera.id
        
        datos={
            'año':an.nombre,
            'año_id':id_an,
            'semestre':semestre.nombre,
            'carrera_nombre':carrn,
            'carrera_id':carrid,
            }
           
        dato=json.dumps(datos)
        
        return HttpResponse(dato, content_type="application/json")
        
    else:
        raise Http404   