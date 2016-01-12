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
from .utiles import *
from datetime import *
from django.core.serializers import serialize
import json


from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from .utiles import login_required

#Se han hecho cambios en este m'etodo respecto al oriiginal
def login(request):   
    next =  '/'
    

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            django_login(request, user)
            User.objects.get(username=username)
            return HttpResponseRedirect(next)
       
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)

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


def eliminar_carrera(request, id):
    car=Carrera.objects.get(id=id)
    car.delete()
    return HttpResponseRedirect(reverse('home'))


@login_required
def user_create(request):

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
        actual = request.META.get('HTTP_REFERER', None) or '/'
        return  HttpResponseRedirect(actual) 
           




#datos del planificador
@login_required
def data_user_update(request):
    
    id=int(request.GET['id'])
    use=User.objects.get(id=id)
    
    datos={
        'id':use.id,
        'nombre':use.first_name,
        'apellidos':use.last_name,
        'usuario':use.username,
        'email':use.email,
        
    } 
    datoss=json.dumps(datos)
    return HttpResponse(datoss, content_type="application/json")
 
#actualizando planificador           
@login_required
def actualizar_planificador(request, id):
    
    use=User.objects.get(id=id)
   
    use.first_name=request.POST['first_name']
    use.last_name=request.POST['last_name']
    use.username=request.POST['username']
    use.email=request.POST['email']
    use.set_password(request.POST['password'])
           
    use.save();
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
    
              
#Eliminar Usuarios
@login_required
def user_delete(request,id):
    actual = request.META.get('HTTP_REFERER', None) or '/'
    e= User.objects.filter(id=id)
    e.delete()
    return HttpResponseRedirect(actual)



@login_required
def crear_profesor(request):
    if request.POST:
       nombre=request.POST['nombre']
       titulo=request.POST['titulo']
       
       try:
           profesor=Profesor.objects.get(nombre=nombre,titulo=titulo)
       except ObjectDoesNotExist:
           profesor=Profesor(nombre=nombre, titulo=titulo)
           profesor.save()
       
       actual = request.META.get('HTTP_REFERER', None) or '/'
       return  HttpResponseRedirect(actual)    
           
                
@login_required
def eliminar_profesor(request,id):
    prof=Profesor.objects.get(id=id)
    prof.delete()
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)  
    
    
    
    
       
@login_required   
def profesor_list(request):
    users = Profesor.objects.all()
    valores=[]
    
    if users:
        for us in users:        
            dat={}
            dat['nombre']=us.nombre
            dat['titulo']=us.titulo
            dat['id']=us.id
            valores.append(dat)
        
    
    datos=json.dumps(valores)
    
    
    return HttpResponse(datos, content_type="application/json")

def data_profesor(request):
    id=int(request.GET['id'])
    profesor=Profesor.objects.get(id=id)
    
    dato={
       'id':profesor.id,
       'nombre':profesor.nombre,
       'titulo':profesor.titulo,
    }
    
    datos=json.dumps(dato)    
    
    return HttpResponse(datos, content_type="application/json")


def actualizar_profesor(request, id):
    profe=Profesor.objects.get(id=id)
    profe.nombre=request.POST['nombre']
    profe.titulo=request.POST['titulo']
    profe.save()
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)



@login_required   
def user_list(request):
    users = User.objects.all()
    valores=[]
    
    if users:
        for us in users:        
            dat={}
            dat['nombre']=us.first_name
            dat['apellido']=us.last_name
            dat['usuario']=us.username
            dat['email']=us.email
            dat['id']=us.id
            valores.append(dat)
        
    
    datos=json.dumps(valores)    
    
    return HttpResponse(datos, content_type="application/json")

   

@login_required
def cambiarPassword(request):

    if request.method == "POST":
        password = request.POST['password']
        usuario = request.user
        usuario.password = password
        usuario.set_password(password)
        usuario.save()
        return HttpResponseRedirect(reverse('home'))
            
 

def crear_asignatura(request):
     if request.POST:
        nombre=request.POST['nombre']
        horas=request.POST['horas']
        identificador=request.POST['identificador']
        id_carrera_año=request.POST['id_carrera_año']
        id_profesor=request.POST['profesor']
        profesor=Profesor.objects.get(id=id_profesor)
        carrera_año=CarreraAño.objects.get(id=id_carrera_año)
        
        try:            
            asig=Asignatura.objects.get(
                id_profesor=id_profesor,
                nombre=nombre,
                horas=horas,
                identificador=identificador,
                id_carrera_año=id_carrera_año,
            )
        except ObjectDoesNotExist:
            asig=Asignatura(
                id_profesor=profesor,
                nombre=nombre,
                horas=horas,
                identificador=identificador,
                id_carrera_año=carrera_año,
                )
            asig.save()
            
        actual = request.META.get('HTTP_REFERER', None) or '/'
        return  HttpResponseRedirect(actual)
            
 
 
def actualizar_asignatura(request, id):
    asignatura=Asignatura.objects.get(id=id) 
    asignatura.nombre=request.POST['nombre']
    asignatura.horas=request.POST['horas']
    asignatura.identificador=request.POST['identificador']
    
    id_carrera_año=request.POST['id_carrera_año']
    id_profesor=request.POST['profesor']
    profesor=Profesor.objects.get(id=id_profesor)
    carrera_año=CarreraAño.objects.get(id=id_carrera_año) 
 
    asignatura.id_carrera_año=carrera_año
    asignatura.id_profesor=profesor
    asignatura.save()
    
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
    
 
            
 #id carrera_año   
def lista_asignaturas(request,id):
    asignaturas=Asignatura.objects.filter(id_carrera_año=id)
    
    valores=[]
    for asignatura in asignaturas:
        
        datos={}
        datos['nombre']=asignatura.nombre
        datos['identificador']=asignatura.identificador
        datos['horas']=asignatura.horas
        datos['id']=asignatura.id
        datos['profesor']=asignatura.id_profesor.nombre + " (" + asignatura.id_profesor.titulo + ")"
        valores.append(datos)
        
    dato=json.dumps(valores)
     
    return HttpResponse(dato, content_type="application/json")   
                    
def data_asignatura(request):
    id=int(request.GET['id'])
    asignatura=Asignatura.objects.get(id=id)
    
    dato={
        'nombre':asignatura.nombre,
        'identificador':asignatura.identificador,
        'horas':asignatura.horas,
        'profesor':asignatura.id_profesor.id
    }
    
    datos=json.dumps(dato)   
    return HttpResponse(datos, content_type="application/json")

          
            

def crear_semana(request):
    de=request.POST['desde'].split("-")
    d=int(de[0])
    m=int(de[1])
    a=int(de[2])
    
    numero=str(request.POST['numero'])
    carra=int(request.POST['año'])
    carrera=int(request.POST['carrera'])
    caa=CarreraAño.objects.get(id=carra)
    car=Carrera.objects.get(id=carrera)
    can_sem=int(request.POST['cantidad_sem'])
    
    dt=date(d,m,a)
            
    try:   
        sem = Semana.objects.get(
            desde = dt,
            numero=numero,
            id_carrera_año=carra,
            id_carrera=carrera,
            )
    except ObjectDoesNotExist:
        sem=Semana(
            desde = dt,
            numero=numero,
            id_carrera_año=caa,
            id_carrera=car,
            )
        sem.save()
        
        fch=dt                      
        smn=sem
        cont=0        
        can_sem=int(can_sem)*5
        for i in range(can_sem):
            dy=fch.day
            mt=fch.month
            yr=fch.year
            
            if cont == 5:
                fch=calendar(dy,mt,yr,2) 
                sm=Semana(
                    desde=fch,
                    numero=int((i+1)/5)+1,
                    id_carrera_año=caa,
                    id_carrera=car,
                    )
                    
                sm.save() 
                smn=sm 
                dy=fch.day
                mt=fch.month
                yr=fch.year
                cont=0                                    
              
            dias=Dia(fecha=fch, id_semana=smn)
            dias.save()
            fch=calendar(dy,mt,yr,1)
            cont+=1
               
    
    return  HttpResponseRedirect('/administracion/crear_horario/'+str(carra)+'/')
     



def eliminar_asignatura(request,id):
    asignatura=Asignatura.objects.get(id=id)
    asignatura.delete()
            
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
     

#id carreraaño        
def crear_horario(request, id):
    smna=Semana.objects.filter(id_carrera_año=id)
    
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
      
    #aux=""
    #lists = [[] for i in range(1,91)]
    #for li in lists:
    #    for i in range(5):
    #        aux+="<td name=\"selda\"><a href=\"\"class=\"btn btn-default\">Añadir</a> </td>"
    #    li.append(aux)
    #    aux=""
    
    asignaturas=Asignatura.objects.filter(id_carrera_año=id)
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
    if request.user.is_authenticated():
        return render_to_response('crear_horario.html',auxi,RequestContext(request))
    else:
        return render_to_response('vista_horario.html',auxi,RequestContext(request))      
    #crear horario ver
    
def crear_turno(request):
    asigna_id=int(request.POST['asignatura'])
    tip_id=int(request.POST['tipp'])
    di=int(request.POST['diass'])
    
    asignatura=Asignatura.objects.get(id=asigna_id)
    tipo=Tipo.objects.get(id=tip_id)
    tn=str(request.POST['turnoo'])
    dia=Dia.objects.get(id=di)
    
    try:
        tur=Turno.objects.get(id_dia=di,id_asignatura=asigna_id,id_tipo=tip_id,turno=tn)
    except ObjectDoesNotExist:
        tur=Turno(id_dia=dia,id_asignatura=asignatura,id_tipo=tipo,turno=tn)
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
    
def eliminar_facultad(request, id):
    facu=Facultad.objects.get(id=id)
    facu.delete()
    return HttpResponseRedirect(reverse('home'))
     
 
def is_semana(request):
    if request.is_ajax:
        id_an=int(request.GET['id'])
        sem=Semana.objects.filter(id_carrera_año=id_an)
        
        semanas=False
        if sem:
            semanas=True
        
        aux={'semana':semanas}
        
        dato=json.dumps(aux)
        
        return HttpResponse(dato, content_type="application/json")
        
    else:
        raise Http404   
        
     
 
    
def infomacion_preimera_semana(request):
    if request.is_ajax:
               
        id_ca=int(request.GET['id'])
        ca=CarreraAño.objects.get(id=id_ca)
        anhos=Año.objects.get(id=ca.id_año.id)
        semestre = Semestre.objects.get(id=anhos.id_semestre.id)
        
        carrn=ca.id_carrera.nombre
        carrid=ca.id_carrera.id
        
        datos={
            
            'año_id':id_ca,
            'semestre':semestre.nombre,
            'carrera_nombre':carrn,
            'carrera_id':carrid,
            }
           
        dato=json.dumps(datos)
        
        return HttpResponse(dato, content_type="application/json")
        
    else:
        raise Http404   
        
def isLunes(request):
    valor=request.GET['dato']    
    valor=valor.split('-')
     
    dia=dias_semana(int(valor[2]), int(valor[1]), int(valor[0]))
    
    dato=False
    if dia=='Lunes':
        dato=True
        
    datos={
        'islunes':dato,
    } 
    datoss=json.dumps(datos)
    return HttpResponse(datoss, content_type="application/json")
        
       
def cambiar_fecha(request):
    id_fecha_antigua=int(request.POST['id_fecha_antigua'] )  
    fecha_actual=request.POST['fecha_actual']
    id_carrera_año=int(request.POST['id_carrera_año'])
    
    fecha=fecha_actual.split('-')
    
    fechaac=date(int(fecha[0]),int(fecha[1]),int(fecha[2]))
    
    
    dia=Dia.objects.get(id=id_fecha_antigua) 
    numero_semana_primero=dia.id_semana.numero
      
    semana=Semana.objects.filter(id_carrera_año=id_carrera_año)
    
    dias_cambiar=[]
    for sem in semana:
        if sem.numero >=  numero_semana_primero:
            dias_cambiar+=Dia.objects.filter(id_semana=sem.id)
    
       
    resta=fechaac - dia.fecha
    resta=resta.days    
    
    
    for d in dias_cambiar:
        f=d.fecha + timedelta(days=resta)
               
        print(f)
        d=Dia(id=d.id,fecha=f,id_semana=d.id_semana)
        d.save()
        
        
    datos={
        'informacion':'Fecha Cambiada',
    } 
    datoss=json.dumps(datos)
    return HttpResponse(datoss, content_type="application/json")
            
    
    
def eliminar_turno(request, id):
    tur=Turno.objects.get(id=id)
    tur.delete()
    
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
 
def retornar(request):
    actual = request.META.get('HTTP_REFERER', None) or '/'
    return  HttpResponseRedirect(actual)
                    