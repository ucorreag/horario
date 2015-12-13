from django.conf.urls import  url

urlpatterns = [
	url(r'login/$','apps.administracion.views.login',name='login'),
    url(r'logout/$','apps.administracion.views.logout', name='logout'),
    url(r'lista_usuarios/$','apps.administracion.views.user_list',name='lista_usuarios'),
    url(r'detalles/(?P<id>\d+)/$','apps.administracion.views.user_detail',name='usuario'),
    url(r'eliminar_usuario/(?P<id>\d+)/$','apps.administracion.views.user_delete',name='eliminar'),
    url(r'crear_usuario/$','apps.administracion.views.user_create', name='crear_usuario'),
    url(r'administracion/actualizar_usuario/(?P<id>\d+)/$','apps.administracion.views.user_update',name='actualizar'),
    url(r'CambiarPassword/$', 'apps.administracion.views.cambiarPassword',name='CambiarPassword'),
      
	]