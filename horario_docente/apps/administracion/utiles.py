
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from datetime import *
import calendar as Calendario

# Create your views here.
def login_required(function):
    def wrapper(*args,**kwargs):
        request = args[0]
        if not request.user.is_authenticated() and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('login'))
        elif request.user.is_authenticated() and not request.user.is_superuser:
            logout(request)
            return HttpResponseRedirect(reverse('login'))
        else:
            return function(*args,**kwargs)
    return wrapper

def calendar(dy, mt, yr, suma):
    for i in range(suma):
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
        elif mt==7 and dy>31:
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
    return date(yr,mt,dy)           


#dias de la semana
def dias_semana(dia, mes, año):
    aux=Calendario.weekday(año, mes, dia)
    dias=""
    if aux==0:
        dias='Lunes'
    elif aux==1:
        dias='Martes'
    elif aux==2:
        dias='Miércoles'
    elif aux==3:
        dias='Jueves'
    elif aux==4:
        dias='Viernes'
    elif aux==5:
        dias='Sábado'
    elif aux==6:
        dias='Domingo'       
    return dias 