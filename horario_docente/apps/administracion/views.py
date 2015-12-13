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

    user = User.objects.get(id=id)

    return render_to_response(
        'Detalles_Usuario.html',
        {
            'p': _('Detalles del Usuario'),
            'user':user,
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
         carrera=Carrera(nombre)
         carrera.save()
    
     return render_to_response('Lista_carreras.html',{'carreras':carreras},RequestContext(request))
     
         
         