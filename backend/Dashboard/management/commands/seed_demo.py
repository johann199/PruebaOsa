from datetime import date, timedelta
import uuid

from django.core.management.base import BaseCommand

from Cliente.models import Cliente
from Factura.models import Factura
from Usuario.models import Usuario


class Command(BaseCommand):
    help = "Carga los datos de ejemplo de la prueba técnica (clientes, facturas, usuario analista)"

    def handle(self, *args, **options):
        hoy = date.today()

        clientes_facturas = [
            {
                "nombre_empresa": "Industrias Alfa",
                "nit": "900123456",
                "promedio_dias_pago": 60,
                "correo": "alfa@industriasalfa.com",
                "factura": {
                    "numero_factura": "F-1045",
                    "fecha_vencimiento": hoy - timedelta(days=45),
                    "valor": 85000000,
                    "estado": "Vencida",
                },
            },
            {
                "nombre_empresa": "Comercial Beta",
                "nit": "900234567",
                "promedio_dias_pago": 0,
                "correo": "contacto@comercialbeta.com",
                "factura": {
                    "numero_factura": "F-1080",
                    "fecha_vencimiento": hoy,
                    "valor": 120000000,
                    "estado": "Pendiente",
                },
            },
            {
                "nombre_empresa": "Distribuidora Gamma",
                "nit": "900345678",
                "promedio_dias_pago": 120,
                "correo": "finanzas@distribuidoragamma.com",
                "factura": {
                    "numero_factura": "F-0990",
                    "fecha_vencimiento": hoy - timedelta(days=95),
                    "valor": 45000000,
                    "estado": "Vencida",
                },
            },
            {
                "nombre_empresa": "Servicios Delta",
                "nit": "900456789",
                "promedio_dias_pago": 0,
                "correo": "cartera@serviciosdelta.com",
                "factura": {
                    "numero_factura": "F-1102",
                    "fecha_vencimiento": hoy + timedelta(days=15),
                    "valor": 60000000,
                    "estado": "Pendiente",
                },
            },
            {
                "nombre_empresa": "Tech Omega",
                "nit": "900567890",
                "promedio_dias_pago": 30,
                "correo": "facturacion@techomega.com",
                "factura": {
                    "numero_factura": "F-1055",
                    "fecha_vencimiento": hoy - timedelta(days=10),
                    "valor": 30000000,
                    "estado": "Pendiente",
                },
            },
        ]

        creados = 0
        for c in clientes_facturas:
            cliente, created = Cliente.objects.get_or_create(
                nit=c["nit"],
                defaults={
                    "nombre_empresa": c["nombre_empresa"],
                    "promedio_dias_pago": c["promedio_dias_pago"],
                    "correo": c["correo"],
                    "token": uuid.uuid4(),
                    "creado": hoy,
                    "modificado": hoy,
                },
            )
            if created:
                creados += 1

            f = c["factura"]
            if not Factura.objects.filter(numero_factura=f["numero_factura"]).exists():
                Factura.objects.create(
                    numero_factura=f["numero_factura"],
                    fecha_emision=f["fecha_vencimiento"] - timedelta(days=30),
                    fecha_vencimiento=f["fecha_vencimiento"],
                    valor=f["valor"],
                    cliente=cliente,
                    estado=f["estado"],
                    creado=hoy,
                    modificado=hoy,
                )

        if not Usuario.objects.filter(correo="analista@pruebaosa.com").exists():
            Usuario.objects.create(
                nombre="Analista Cartera",
                rol="Gestor",
                correo="analista@pruebaosa.com",
                password="admin123",
                creado=hoy,
                modificado=hoy,
            )

        self.stdout.write(self.style.SUCCESS(f"{creados} clientes creados y 5 facturas cargadas."))
        for c in Cliente.objects.all():
            self.stdout.write(f"Portal {c.nombre_empresa}: http://localhost:4200/estado-cuenta/{c.token}")
        self.stdout.write(self.style.SUCCESS("Login analista: analista@pruebaosa.com / admin123"))