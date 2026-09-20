from django.shortcuts import render, get_object_or_404, redirect
from ninja import Router
from typing import List
from .schemas import RecaudoIn, RecaudoOut
from .models import Recaudo

recuado = Router()

@recuado.post("/recaudo")
def crear_recaudo(request, payload: RecaudoIn):
    recaudo = Recaudo.objects.create(**payload.dict())
    return {"id": recaudo.id}

@recuado.get("/recaudos", response=List[RecaudoOut])
def consultar_recaudos(request):
    qs = Recaudo.objects.all()
    return qs

@recuado.put("/recaudo/{recaudo_id}")
def actualizar_recaudo(request, recaudo_id: int, payload: RecaudoIn):
    recaudo = get_object_or_404(Recaudo, id=recaudo_id)
    for attr, value in payload.dict().items():
        setattr(recaudo, attr, value)
    recaudo.save()
    return {"success": True}

@recuado.delete("/recaudo/{recaudo_id}")
def eliminar_recaudo(request, recaudo_id: int):
    recaudo = get_object_or_404(Recaudo, id=recaudo_id)
    recaudo.delete()
    return {"success": True}
