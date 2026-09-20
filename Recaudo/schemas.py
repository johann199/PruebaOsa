from datetime import date
from ninja import Schema

class RecaudoIn(Schema):
    fecha_recaudo: date = None
    valor_recaudo: int
    factura: int = None
    creado: date = None
    modificado: date = None
    
class RecaudoOut(Schema):
    id: int
    fecha_recaudo: date = None
    valor_recaudo: int
    factura: int = None
    creado: date = None
    modificado: date = None