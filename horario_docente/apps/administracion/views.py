from gettext import gettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import  User,Group
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from apps.horario.models import *
from datetime import *


from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from .utiles import login_required


USER_ROLES = (
  (0x01, _('Planificador')),
  (0x02, _('Profesor')),
)
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

@login_required
def user_detail(request,id):

    usuario = User.objects.get(id=id)

    return render_to_response(
        'Detalles_Usuario.html',
        {
            'p': _('Detalles del Usuario'),
            'usuario':usuario,
            },
        RequestContext(request)
    )
#Crear Usuarios
@login_required
def user_create(request):

    context = {
        'p': _('Crear Usuario'),
        'roles': USER_ROLES,
        }
    if request.POST:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        role = int(request.POST['role'])        
        password = request.POST['password']

                
        if User.objects.filter(username=username).exists():

            context['error'] = _('El nombre de usuario seleccionado ya existe')
            context['username'] = username
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email
            context['role'] = role
           
        else:
                g=Group.objects.filter(id=role)

                user= User.objects.create_user(username, email,  password)
                user.first_name= first_name
                user.last_name = last_name
                user.is_staff=True
                user.groups=g
                user.role=role
                
                if role==1:
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
        role = int(request.GET['role'])
        password = request.GET['password']
        print(role)
        gr=Group.objects.filter(id=role)
        use.first_name= first_name
        use.last_name = last_name
        use.is_staff=True
        use.groups=gr
        use.role=role
        if role==1:
            use.is_superuser=True
        use.save()
        return HttpResponseRedirect('/administracion/lista_usuarios/')
    
    else:
        return render_to_response(
             'Modificar_Usuario.html',
            {
                'p': _('Actualizar Usuario ' +use.username+''),
                'usuario':use,
                'roles': USER_ROLES,
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
        
 #crear carreras
@login_required
def lista_carreras(request):
    carreras=Carrera.objects.all()
    if request.POST:
        nombre=request.POST['nombre']
        carrera=Carrera(nombre=nombre)
        carrera.save()
        
        año=Año.objects.all()
        for an in año:
            m=CarreraAño(id_carrera=carrera, id_año=an)
            m.save()
    
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
    semestre=int(request.POST['semestre'])
    carrera=int(request.POST['carrera'])
    seme=Semestre.objects.get(id=semestre)
    car=Carrera.objects.get(id=carrera)
    
    dt=date(d,m,a)
    sem=Semana(
        desde = dt,
        numero=numero,
        id_semestre=seme,
        id_carrera=car,
        )
        
    try:   
        semanas=Semana.objects.get(desde = dt,
            numero=numero,
            id_semestre=semestre,
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
                    id_semestre=seme,
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
        
        
def crear_horario(request, id):
    seman=Semana.objects.filter(id_semestre=id)
    
    x=None
    if seman !=[]:
        x=seman[0]
        for i in seman:
            if x.desde > i.desde:
                x=i             
            
    semana=x
    
    
    smna=Semana.objects.filter(id_semestre=id)
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
    
    auxi={
        'lists':contacts,
         'seman':semana ,
         'turnos':turnos,
         'asignaturas':asignaturas,
         'tipos':tipos,
         'isturno':isturno,
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
           