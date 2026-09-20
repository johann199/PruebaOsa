from datetime import date
from django.shortcuts import render, get_object_or_404
from ninja import Router
from .models import Cliente
from typing import List
from .schemas import ClienteIn, ClienteOut, VerificarNitIn
from Factura.models import Factura


cliente = Router()
portal_cliente = Router()

@portal_cliente.post("/estado-cuenta/{token}")
def consultar_estado_cuenta(request, token: str, payload: VerificarNitIn):
    cliente = get_object_or_404(Cliente, token=token)

    if cliente.nit != payload.nit:
        return {"error": "NIT incorrecto"}, 403

    facturas = Factura.objects.filter(cliente=cliente)
    hoy = date.today()
    resultado = []
    for f in facturas:
        dias_mora = (hoy - f.fecha_vencimiento).days
        resultado.append({
            "numero_factura": f.numero_factura,
            "fecha_vencimiento": f.fecha_vencimiento,
            "dias_mora": dias_mora if dias_mora > 0 else 0,
            "valor": f.valor,
            "estado": f.estado,
        })

    return {"cliente": cliente.nombre_empresa, "facturas": resultado}

@cliente.post("/cliente")
def crearcliente(request, payload:ClienteIn):
    cliente = Cliente.objects.create(**payload.dic())
    return {"id": cliente.id}

@cliente.get("/clientes", response=List[ClienteOut])
def consultarclientes(request):
    qs = Cliente.objects.all()
    return qs

@cliente.put("/clientes/{cliente_id}")
def actualizarcliente(request, cliente_id: int, payload:ClienteIn):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    for attr, value in payload.dic().items():
        setattr(cliente, attr, value)
    cliente.save()
    return {"success": True}

@cliente.delete("/cliente/{cliente_id}")
def eliminarcliente(request, cliente_id: int):
    cliente = get_object_or_404(Cliente, id= cliente_id)
    cliente.delete()
    return {"success": True}

