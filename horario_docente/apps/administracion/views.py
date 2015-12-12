from gettext import gettext as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import  User,Group
from django.views.generic.edit import CreateView
from django.views.generic import FormView



from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from .utiles import login_required


USER_ROLES = (
  (0x01, _('Planificador')),
  (0x02, _('Estudiante')),
  (0x03, _('Profesor')),
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
    return HttpResponseRedirect('/administracion/login/')
#Detalles de Usuarios

def user_detail(request,id):

    user = User.objects.filter(id=id)

    return render_to_response(
        'Detalles_Usuario.html',
        {
            'p': _('Detalles del Usuario'),
            'user':user[0],
            },
        RequestContext(request)
    )
#Crear Usuarios
def user_create(request):

    context = {
        'p': _('Crear Usuario'),
        'roles': USER_ROLES,
        }
    if request.POST:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role = int(request.POST['role'])
        password = request.POST['password']

                
        if User.objects.filter(username=username).exists():

            context['error'] = _('El nombre de usuario seleccionado ya existe')
            context['username'] = username
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['role'] = role
           
        else:
                g=Group.objects.filter(id=role)

                user= User.objects.create_user(username, username+'@uho.cu',  password)
                user.first_name= first_name
                user.last_name = last_name
                user.is_staff=True
                user.groups=g
                user.role=role
                
                if role==1:
                    user.is_superuser=True
                user.save()

                return HttpResponseRedirect('/administracion/lista_usuarios/')

    return render_to_response(
        'Crear_Usuario.html',
        context,
        RequestContext(request)
    )




#Modificar Usuarios

def user_update(request,id):
    use=User.objects.get(id=id)
    if use.groups==1:
        #IMPLEMNTAR
        user=User.objects.filter(id=id)
        #users = get_object_or_404(User, pk=id)
        if request.GET:
            username = request.GET['username']
            first_name = request.GET['first_name']
            last_name = request.GET['last_name']
            role = int(request.GET['role'])
            password = request.GET['password']
            user.delete()
            g=Group.objects.filter(id=role)
            user= User.objects.create_user(username, username+'@uho.edu.cu',  password)
            user.first_name= first_name
            user.last_name = last_name
            user.is_staff=True
            user.groups=g
            user.role=role
            if role==1:
                user.is_superuser=True
            user.save()
            
            return HttpResponseRedirect('/administracion/lista_usuarios/')
        else:   
            return render_to_response(
            'Modificar_Usuario.html',
            {
                'p': _('Actualizar Usuario ' +user.get().username+''),
                'usuario':user,
                'roles': USER_ROLES,
                },
            RequestContext(request)
        )
        user_create()
    else:
        return HttpResponseRedirect('/')
   
#Eliminar Usuarios
def user_delete(request,id):
    actual = request.META.get('HTTP_REFERER', None) or '/'

    try:
        e= User.objects.filter(id=id)
        e.delete()
        return HttpResponseRedirect(actual)
    except ObjectDoesNotExist:
        error_msg = "El sujeto no existe."
    return render_to_response(
         'Eliminar.html',
         {
             'page_title': _('Eliminar Usuario #'),
         },
         RequestContext(request)
    )
def user_list(request):
    users = User.objects.all()
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
             'page_title': _('Eliminar Usuario #'),

             'contacts':contacts,
         },
         RequestContext(request)
    )

def cambiarPasswordProfesor(request,aprobado = ""):

    if request.method == "POST":
        form = passwordForm(request.POST,request.FILES)
        if form.is_valid():
                password = form.cleaned_data['password']
                usuario = request.user
                usuario.password = password
                usuario.set_password(form.cleaned_data['password'])
                usuario.save()
                return HttpResponseRedirect('/')
                
                
                form = passwordForm()
                ctx = {'form':form}
                return render_to_response('CambiarPasswordP.html',ctx,context_instance = RequestContext(request))
        else:
            form = passwordForm()
            ctx = {'form':form,'aprobado':aprobado}
            return render_to_response('CambiarPasswordP.html',ctx,context_instance = RequestContext(request))
    else:
        form = passwordForm()
        ctx = {'form':form,'aprobado':aprobado}
        return render_to_response('CambiarPasswordP.html',ctx,context_instance = RequestContext(request))



   
def cambiarPasswordEstudiante(request,aprobado = ""):

    if request.method == "POST":
        form = passwordForm(request.POST,request.FILES)
        if form.is_valid():
                password = form.cleaned_data['password']
                usuario = request.user
                usuario.password = password
                usuario.set_password(form.cleaned_data['password'])
                usuario.save()
                return HttpResponseRedirect('/')
                
                
                form = passwordForm()
                ctx = {'form':form,'aprobado':aprobado}
                return render_to_response('CambiarPasswordE.html',ctx,context_instance = RequestContext(request))
        else:
            form = passwordForm()
            ctx = {'form':form,'aprobado':aprobado}
            return render_to_response('CambiarPasswordE.html',ctx,context_instance = RequestContext(request))
    else:
        form = passwordForm()
        ctx = {'form':form,'aprobado':aprobado}
        return render_to_response('CambiarPasswordE.html',ctx,context_instance = RequestContext(request))
  
 
 
 