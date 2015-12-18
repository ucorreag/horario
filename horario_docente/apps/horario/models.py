#-*-charset=utf-8-*-

from django.db import models
from django.contrib.auth.models import  User
from datetime import date


# formato 2013-2014
class Curso(models.Model):
	desde=models.CharField(max_length=4)
	hasta=models.CharField(max_length=4, editable=False)
	
	def save(self):
		self.hasta=int(self.desde)+1
		super(Curso, self).save(*args, **kwargs)
	
	def __str__(self):
		return 	self.desde+"|"+self.hasta
		
class Carrera(models.Model):
	nombre=models.CharField(max_length=100, verbose_name="Carrera")
	
	def __str__(self):
		return self.nombre
		
class CarreraCurso(models.Model):
	id_curso=models.ForeignKey(Curso)
	id_carrera=models.ForeignKey(Carrera)

#1°, 2°, 3°...
class Año(models.Model):
	nombre=models.CharField(max_length=10,choices=(('1','primero'),('2','segundo'),('3','tercero'),('4','cuarto'),('5','quinto')))

	def __str__(self):
		return self.nombre

class CarreraAño(models.Model):
	id_carrera=models.ForeignKey(Carrera)
	id_año=models.ForeignKey(Año)	
	
class Semestre(models.Model):
	nombre=models.CharField(max_length=20,choices=(('1','primero'),('2','segundo')))
	id_año=models.ForeignKey(Año)
	
	def __str__(self):
		return self.nombre+"|"+self.id_anho.__str__()

class Semana(models.Model):
	desde=models.DateField()
	hasta=models.DateField(editable=False)
	numero=models.CharField(max_length=10, verbose_name="Numero de Semana")
	id_semestre=models.ForeignKey(Semestre)
	id_carrera=models.ForeignKey(Carrera)
	
	def save(self):
		aux=self.desde
		dia = aux.day
		mes = aux.month
		año = aux.year
		for h in range(4):
			dia+=1 #segun el mes 
			if mes==1 and dia>31:
				dia = 1
				mes = 2
			elif mes == 2 and dia > 29 :
				dia = 1
				mes = 3
			elif mes==3 and dia > 31:
				dia=1
				mes=4
			elif mes==4 and dia>30:
				dia=1
				mes=5
			elif mes==5 and dia>31:
				dia=1
				mes=6
			elif mes==6 and dia>30:
				dia=1
				mes=7
			elif mes==7 and dia>31:
				dia=1
				mes=8
			elif mes==8 and dia>31:
				dia=1
				mes=9
			elif mes==9 and dia>30:
				dia=1
				mes=10
			elif mes==10 and dia>31:
				dia=1
				mes=11
			elif mes==11 and dia>30:
				dia=1
				mes=12
			elif mes==12 and dia>31:
				dia=1
				mes=1
				año+=1
		aux=aux.replace(day = dia, month=mes, year=año)	
		self.hasta=aux
		super(Semana,self).save(date)
	
	def __str__(self):
		return self.numero
	
class Dia(models.Model):
	fecha=models.DateField()
	id_semana=models.ForeignKey(Semana)
	
#un profesor puede tener varias asignaturas
class Asignatura(models.Model):
	id_profesor=models.ForeignKey(User,limit_choices_to={'groups': 3})
	nombre=models.CharField(max_length=50)
	horas=models.IntegerField()
	id_semestre=models.ForeignKey(Semestre)
	id_carrera=models.ForeignKey(Carrera)
	
	def __str__(self):
		return self.nombre


class Tipo(models.Model):
	nombre=models.CharField(max_length=20)
	
	def __str__(self):
		return self.nombre
		
class AsignaturaTipo(models.Model):
	id_asignatura=models.ForeignKey(Asignatura)
	id_tipo=models.ForeignKey(Tipo)
	
class Turno(models.Model):
	id_dia=models.ForeignKey(Dia)
	id_asignatura_tipo=models.ForeignKey(AsignaturaTipo)
	turno=models.CharField(max_length=20)
	