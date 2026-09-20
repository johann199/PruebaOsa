from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from Recaudo.views import recuado
from Factura.views import factura
from Usuario.views import usuario
from Cliente.views import cliente, portal_cliente
from Dashboard.views import dashboard

api = NinjaAPI()

api.add_router("/recaudo/", recuado)
api.add_router("/factura/", factura)
api.add_router("/usuario/", usuario)
api.add_router("/cliente/", cliente)
api.add_router("/portal-cliente/", portal_cliente)
api.add_router("/dashboard/", dashboard)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
