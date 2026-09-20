from datetime import date
from ninja import Schema


class UsuarioIn(Schema):
    nombre: str
    rol: int = None
    correo: str
    password: str
    creado: date = None
    modificado: date = None
    

class UsuarioOut(Schema):
    id: int
    nombre: str
    rol: str = None
    correo: str
    creado: date = None
    modificado: date = None


class LoginIn(Schema):
    correo: str
    password: str


class LoginOut(Schema):
    id: int
    nombre: str
    rol: str = None
    correo: str
    
    

    
    