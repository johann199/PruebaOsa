from datetime import date
from ninja import Schema

class RecaudoIn(Schema):
    fecha: date = None
    valor_pagado: int = None
    factura: int = None
    creado: date = None
    modificado: date = None
    
class RecaudoOut(Schema):
    id: int
    fecha: date = None
    valor_pagado: int = None
    factura: int = None
    creado: date = None
    modificado: date = None