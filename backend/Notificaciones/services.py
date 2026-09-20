from datetime import date

from django.conf import settings
from django.template.loader import render_to_string

from .email_send import enviar_correo
from .pdf_generator import generar_pdf_estado_cuenta


def notificar_estado_cuenta(cliente, facturas_pendientes):
    hoy = date.today()
    facturas_data = []
    for f in facturas_pendientes:
        dias_mora = (hoy - f.fecha_vencimiento).days
        facturas_data.append({
            "numero_factura": f.numero_factura,
            "fecha_vencimiento": f.fecha_vencimiento,
            "dias_mora": dias_mora if dias_mora > 0 else 0,
            "valor": f.valor,
            "estado": f.estado,
        })

    link_portal = f"{settings.FRONTEND_URL}/estado-cuenta/{cliente.token}"

    contenido = render_to_string("notificaciones/estado_cuenta.html", {
        "cliente": cliente,
        "facturas": facturas_data,
        "link_portal": link_portal,
    })

    pdf = generar_pdf_estado_cuenta(cliente, facturas_data, link_portal)

    enviar_correo(
        destinatario=cliente.correo,
        asunto=f"Estado de cuenta - {cliente.nombre_empresa}",
        contenido_html=contenido,
        adjuntos=[("estado-cuenta.pdf", pdf.getvalue(), "application/pdf")],
    )