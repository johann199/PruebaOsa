from django.shortcuts import render, get_object_or_404
from ninja import NinjaAPI
from .models import Cliente
from typing import List
from .schema import ClienteIn, ClienteOut


cliente = NinjaAPI()

@cliente.post("/cliente")
def crearcliente(request, payload:ClienteIn):
    cliente = Cliente.objects.create(**payload.dic())
    return {"id": cliente.id}

@cliente.get("/clientes", response=List[ClienteOut])
def consultarclientes(request):
    qs = Cliente.objects.all()
    return qs

@cliente.put("/clientes/{cliente_id}")
def actualizarcliente(request, cliente_id: id, payload:clienteIn):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    for attr, value in payload.dic().items():
        setattr(cliente, attr, value)
    cliente.save()
    return {"souccess": True}

@cliente.delete("/cliente/{cliente_id}")
def eliminarcliente(request, cliente_id: int):
    cliente = get_object_or_404(Cliente, id= cliente_id)
    cliente.delete()
    return {"success": True}

