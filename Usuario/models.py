from django.db import models

ROL = {"1":"Administrador", "2":"Gestor"}

class Usuario(models.Model):
    id = models.UniqueConstraint(null= False, blank= False)
    nombre = models.CharField(max_length=200)
    rol = models.CharField(ROL["1"])
    correo = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    creado = models.DateField()
    modificado = models.DateField()
    
    
    
