from django.shortcuts import render, get_object_or_404
from ninja import Router
from .models import Usuario
from typing import List
from .schema import UsuarioIn, UsuarioOut


usuario = Router()

@usuario.post("/usuario")
def crearUsuario(request, payload:UsuarioIn):
    usuario = Usuario.objects.create(**payload.dic())
    return {"id": usuario.id}

@usuario.get("/usuarios", response=List[UsuarioOut])
def consultarUsuarios(request):
    qs = Usuario.objects.all()
    return qs

@usuario.put("/usuarios/{usuario_id}")
def actualizarUsuario(request, usuario_id: int, payload:UsuarioIn):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    for attr, value in payload.dic().items():
        setattr(usuario, attr, value)
    usuario.save()
    return {"success": True}

@usuario.delete("/usuario/{usuario_id}")
def eliminarUsuario(request, usuario_id: int):
    usuario = get_object_or_404(Usuario, id= usuario_id)
    usuario.delete()
    return {"success": True}
