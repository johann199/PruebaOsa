from datetime import date
import uuid
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

    hoy = date.today()
    facturas = Factura.objects.filter(cliente=cliente).order_by("fecha_vencimiento")
    resultado = []
    total_pendiente = 0
    for f in facturas:
        dias_mora = (hoy - f.fecha_vencimiento).days
        pendiente = f.estado != "Pagada"
        if pendiente:
            total_pendiente += f.valor
        resultado.append({
            "numero_factura": f.numero_factura,
            "fecha_vencimiento": f.fecha_vencimiento,
            "dias_mora": dias_mora if dias_mora > 0 else 0,
            "valor": f.valor,
            "estado": f.estado,
        })

    return {"cliente": cliente.nombre_empresa, "nit": cliente.nit, "total_pendiente": total_pendiente, "facturas": resultado}

@cliente.post("/cliente")
def crearcliente(request, payload:ClienteIn):
    data = payload.dict()
    if not data.get("token"):
        data["token"] = uuid.uuid4()
    if not data.get("creado"):
        data["creado"] = date.today()
    if not data.get("modificado"):
        data["modificado"] = date.today()
    cliente = Cliente.objects.create(**data)
    return {"id": cliente.id, "token": str(cliente.token)}

@cliente.get("/clientes", response=List[ClienteOut])
def consultarclientes(request):
    qs = Cliente.objects.all()
    return qs

@cliente.put("/clientes/{cliente_id}")
def actualizarcliente(request, cliente_id: int, payload:ClienteIn):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    for attr, value in payload.dict().items():
        setattr(cliente, attr, value)
    cliente.save()
    return {"success": True}

@cliente.delete("/cliente/{cliente_id}")
def eliminarcliente(request, cliente_id: int):
    cliente = get_object_or_404(Cliente, id= cliente_id)
    cliente.delete()
    return {"success": True}

