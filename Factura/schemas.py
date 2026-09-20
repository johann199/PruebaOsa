from datetime import date
from ninja import Schema


class FacturaIn(Schema):
    numero_factura: str
    fecha_emision: date = None
    fecha_vencimiento: date = None
    valor: int
    cliente: int = None
    estado: str
    creado: date = None
    modificado: date = None
    

class FacturaOut(Schema):
    id: int
    numero_factura: str
    fecha_emision: date = None
    fecha_vencimiento: date = None
    valor: int
    cliente: int = None
    estado: str
    creado: date = None
    modificado: date = None
    