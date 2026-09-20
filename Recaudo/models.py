from django.db import models
from Factura.models import Factura
class Recaudo(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    valor_pagado = models.DecimalField(max_digits=10, decimal_places=2) 
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='recaudos')
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Recaudo {self.id} - Fecha: {self.fecha} - Valor Pagado: {self.valor_pagado}"
    