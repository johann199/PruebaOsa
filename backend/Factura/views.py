from django.shortcuts import render, get_object_or_404
from ninja import Router
from .models import Factura
from typing import List
from .schemas import FacturaIn, FacturaOut


factura = Router()

@factura.post("/factura")
def crearcliente(request, payload:FacturaIn):
    factura = Factura.objects.create(**payload.dict())
    return {"id": factura.id}

@factura.get("/facturas", response=List[FacturaOut])
def consultarclientes(request):
    qs = Factura.objects.all()
    return qs

@factura.put("/factura/{factura_id}")
def actualizarcliente(request, factura_id: int, payload:FacturaIn):
    factura = get_object_or_404(Factura, id=factura_id)
    for attr, value in payload.dict().items():
        setattr(factura, attr, value)
    factura.save()
    return {"success": True}

@factura.delete("/factura/{factura_id}")
def eliminarcliente(request, factura_id: int):
    factura = get_object_or_404(Factura, id= factura_id)
    factura.delete()
    return {"success": True}

