from django.db import models

class Cliente(models.Model):
    id = models.UniqueConstraint(null= False, blank= False)
    nombre_empresa = models.CharField(max_length=200)
    nit= models.CharField(max_length=100)
    promedio_dias_pago = models.IntegerField()
    correo = models.EmailField(max_length=200)
    token = models.CharField(max_length=100)
    creado = models.DateField()
    modificado = models.DateField()
    
    
    