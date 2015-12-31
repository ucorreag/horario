from django.conf.urls import  url

urlpatterns = [
	url(r'login/$','apps.administracion.views.login',name='login'),
    url(r'logout/$','apps.administracion.views.logout', name='logout'),
    url(r'lista_usuarios/$','apps.administracion.views.user_list',name='lista_usuarios'),
    url(r'lista_profesores/$','apps.administracion.views.profesor_list',name='lista_profesores'),
    #url(r'detalles/(?P<id>\d+)/$','apps.administracion.views.user_detail',name='usuario'),
    url(r'eliminar_usuario/(?P<id>\d+)/$','apps.administracion.views.user_delete',name='eliminar'),
    url(r'crear_usuario/$','apps.administracion.views.user_create', name='crear_usuario'),
    url(r'crear_profesor/$','apps.administracion.views.crear_profesor', name='crear_profesor'),
    url(r'crear_asignatura/$','apps.administracion.views.crear_asignatura', name='crear_asignatura'),
    url(r'islunes/$','apps.administracion.views.isLunes', name='islunes'),
    url(r'cambiarfecha/$','apps.administracion.views.cambiar_fecha', name='cambiarfecha'),
    
    
    
    url(r'actualizar_usuario/(?P<id>\d+)/$','apps.administracion.views.user_update',name='actualizar'),
    url(r'CambiarPassword/$', 'apps.administracion.views.cambiarPassword',name='CambiarPassword'),
    url(r'crear_carrera/(?P<id>\d+)/$','apps.administracion.views.crear_carrera',name="crear_carrera"),
    url(r'lista_carreras/$','apps.administracion.views.lista_carreras', name='lista_carreras'),
    url(r'lista_asignaturas/(?P<id>[^/]+)/$','apps.administracion.views.lista_asignaturas', name='lista_asignaturas'),
    url(r'eliminar_carrera/(?P<id>\d+)/$','apps.administracion.views.eliminar_carrera',name='eliminar_carrera'),
    url(r'eliminar_asignatura/(?P<id>\d+)/$','apps.administracion.views.eliminar_asignatura', name="eliminar_asignatura"), 
	url(r'crear_horario/(?P<id>\d+)/$','apps.administracion.views.crear_horario',name='horario'),
    url(r'crear_semana/$','apps.administracion.views.crear_semana',name="crear_semana"),
    url(r'crear_turno/$','apps.administracion.views.crear_turno', name="crear_turno"),
    url(r'eliminar_turno/(?P<id>\d+)/$','apps.administracion.views.eliminar_turno', name="eliminar_turno"),
    
    
    url(r'crear_facultad/$','apps.administracion.views.crear_facultad',name="crear_facultad"),
   
   
    url(r'issemana/$','apps.administracion.views.is_semana',name="is_semana"),
    url(r'semes/$','apps.administracion.views.infomacion_preimera_semana',name="infomacion_preimera_semana"),   
    ]