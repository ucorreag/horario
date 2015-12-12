from django.db import models

class Curso(models.Model):
<<<<<<< HEAD
    nombre = models.CharField(max_length=25)
    
    def __str__(self):
        return self.nombre
=======
    nombre = models.CharField(max_length=25)
>>>>>>> a6d2dba... Modelos
