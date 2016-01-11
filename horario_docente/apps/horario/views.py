from django.shortcuts import render
from datetime import *
from django.http import HttpResponseRedirect, HttpResponse
import json

# Create your views here.
def periodo(request):
	ahora=date.today()
	
	if(ahora.month >= 9):
		d=ahora
		a=ahora + timedelta(days=365)
	else:
		d=ahora + timedelta(days=-365)
		a=ahora
			
	
	datos={
		'de':d.year,
		'as':a.year,
	}
	
	dato=json.dumps(datos)
	
	return HttpResponse(dato, content_type="application/json")   
    
	