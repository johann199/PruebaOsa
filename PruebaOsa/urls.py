from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from Recaudo.views import recuado
from Factura.views import factura
from Usuario.views import usuario
from Cliente.views import cliente


api = NinjaAPI()

api.add_router("/recaudo/", recuado)
api.add_router("/factura/", factura)
api.add_router("/usuario/", usuario)
api.add_router("/cliente/", cliente)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
