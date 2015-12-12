from django.conf.urls import  url

urlpatterns = [
	url(r'login/$','apps.administracion.views.login',name='login'),
    url(r'logout/$','apps.administracion.views.logout', name='logout'),
    url(r'lista_usuarios/$','apps.administracion.views.user_list',name='lista_usuarios'),
    url(r'detalles/(?P<id>\d+)/$','apps.administracion.views.user_detail',name='usuario'),
    url(r'eliminar_usuario/(?P<id>\d+)/$','apps.administracion.views.user_delete',name='eliminar'),
    url(r'crear_usuario/$','apps.administracion.views.user_create'),
    url(r'administracion/actualizar_usuario/(?P<id>\d+)/$','apps.administracion.views.user_update',name='actualizar'),
    url(r'CambiarPasswordE/(?P<aprobado>[^/]+)/$', 'apps.administracion.views.cambiarPasswordEstudiante',name='cambiarCE'),
    url(r'CambiarPasswordP/$', 'apps.administracion.views.cambiarPasswordProfesor',name='cambiarCP'),
  
	]