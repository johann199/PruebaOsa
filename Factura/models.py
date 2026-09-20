from django.db import models
from Cliente.models import Cliente

ESTADO = [("1", "Pagada"), ("2", "Pendiente"), ("3", "Vencida")]
class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    numero_factura = models.CharField(max_length=20)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    valor = models.IntegerField()
    cliente = models.ForeignKey(Cliente ,on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, choices=ESTADO)
    creado = models.DateField()
    modificado = models.DateField()
    
    def __str__(self):
        return self.numero_factura