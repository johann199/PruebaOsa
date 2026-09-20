from django.conf import settings
from django.core.mail import EmailMessage


def enviar_correo(destinatario: str, asunto: str, contenido_html: str, adjuntos=None):
    correo = EmailMessage(
        subject=asunto,
        body=contenido_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )
    correo.content_subtype = "html"
    for nombre, contenido, mimetype in (adjuntos or []):
        correo.attach(nombre, contenido, mimetype)
    correo.send()