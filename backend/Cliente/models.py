from django.db import models

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=200)
    nit= models.CharField(max_length=100)
    promedio_dias_pago = models.IntegerField()
    correo = models.EmailField(max_length=200)
    token = models.UUIDField(default=None, null=True, blank=True)
    creado = models.DateField()
    modificado = models.DateField()
    
    def __str__(self):
        return f"Cliente {self.id} - Nombre Empresa: {self.nombre_empresa} - NIT: {self.nit}"
    