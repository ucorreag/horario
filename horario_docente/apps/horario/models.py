#-*-charset=utf-8-*-

from django.db import models
from django.contrib.auth.models import  User

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
	
	def save(self):
		aux=self.desde
		dia=aux.desde.day + 4
		aux.day=dia		
		self.hasta=aux
		super(Semana,self).save(*args, **kwargs)
	
	def __str__(self):
		return self.numero
	
class Dia(models.Model):
	fecha=models.DateField()
	
#un profesor puede tener varias asignaturas
class Asignatura(models.Model):
	id_profesor=models.ForeignKey(User,limit_choices_to={'groups': 3})
	nombre=models.CharField(max_length=50)
	tipo=models.CharField(max_length=50, choices=(('conf','conferencia'),('cp','clase práctica'),('sem','seminario'),('lab','laboratorio'),('np','no presencial')))
	
	def __str__(self):
		return self.nombre+"|"+self.tipo

class Turno(models.Model):
	id_dia=models.ForeignKey(Dia)
	id_asignatura=models.ForeignKey(Asignatura)
	turno=models.CharField(max_length=10,choices=(('1','primero'),('2','segundo'),('3','tercero'),('4','cuarto'),('5','quinto'),('6','sexto')))
	
	