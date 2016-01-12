"""horario_docente URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from apps.administracion import urls as adninistracion_urls
from apps.horario import urls as horario_urls


urlpatterns = [
    
    url(r'^$','horario_docente.views.index_view',name="home"),
    
    url(r'^administracion/', include(adninistracion_urls)),
    url(r'^horario/', include(horario_urls)),
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
