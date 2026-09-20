from django.core.management.base import BaseCommand
from Cliente.models import Cliente
from Factura.models import Factura
from Notificaciones.services import notificar_estado_cuenta

class Command(BaseCommand):
    help = "Envía correos de recordatorio a clientes con facturas pendientes/vencidas"

    def handle(self, *args, **options):
        clientes = Cliente.objects.all()
        for cliente in clientes:
            facturas_pendientes = Factura.objects.filter(cliente=cliente, estado__in=["Pendiente", "Vencida"])
            if facturas_pendientes.exists():
                notificar_estado_cuenta(cliente, facturas_pendientes)
                self.stdout.write(f"Correo enviado a {cliente.nombre_empresa}")