from django.db import models
from Cliente.models import Cliente
class Factura(models.Model):
    id = models.IntegerField()
    numero_factura = models.CharField(max_length=20)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    valor = models.IntegerField()
    cliente = models.ForeignKey(Cliente ,on_delete=models.CASCADE)
    estado = models.CharField()
    creado = models.DateField()
    modificado = models.DateField()