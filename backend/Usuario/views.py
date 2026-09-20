from django.shortcuts import render, get_object_or_404
from ninja import Router
from .models import Usuario
from typing import List
from .schema import UsuarioIn, UsuarioOut, LoginIn, LoginOut


usuario = Router()

@usuario.post("/login", response={200: LoginOut, 401: dict})
def login(request, payload: LoginIn):
    usuario = Usuario.objects.filter(correo=payload.correo, password=payload.password).first()
    if not usuario:
        return 401, {"error": "Credenciales incorrectas"}
    return 200, {"id": usuario.id, "nombre": usuario.nombre, "rol": usuario.rol, "correo": usuario.correo}

@usuario.post("/usuario")
def crearUsuario(request, payload:UsuarioIn):
    usuario = Usuario.objects.create(**payload.dict())
    return {"id": usuario.id}

@usuario.get("/usuarios", response=List[UsuarioOut])
def consultarUsuarios(request):
    qs = Usuario.objects.all()
    return qs

@usuario.put("/usuarios/{usuario_id}")
def actualizarUsuario(request, usuario_id: int, payload:UsuarioIn):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    for attr, value in payload.dict().items():
        setattr(usuario, attr, value)
    usuario.save()
    return {"success": True}

@usuario.delete("/usuario/{usuario_id}")
def eliminarUsuario(request, usuario_id: int):
    usuario = get_object_or_404(Usuario, id= usuario_id)
    usuario.delete()
    return {"success": True}
