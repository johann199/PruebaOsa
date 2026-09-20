from datetime import date
from ninja import Schema


class ClienteIn(Schema):
    nombre_empresa: str
    nit: str
    promedio_dias_pago: int
    correo: str
    token: str
    creado: date = None
    modificado: date = None
    

class ClienteOut(Schema):
    id: int
    nombre_empresa: str
    nit: str
    promedio_dias_pago: int
    correo: str
    token: str
    creado: date = None
    modificado: date = None
    
    