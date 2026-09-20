from django.core.mail import send_mail
from django.conf import settings

def enviar_correo(destinatario: str, asunto: str, contenido_html: str):
    send_mail(
        subject=asunto,
        message="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[destinatario],
        html_message=contenido_html,
    )