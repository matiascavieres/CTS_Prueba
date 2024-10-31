from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
import random
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def enviar_correo_verificacion(email, token):
    enlace = f"http://localhost:8000/api/users/verify/{token}/"
    subject = 'Verifica tu cuenta'
    message = f'Por favor verifica tu cuenta haciendo clic en el siguiente enlace: {enlace}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

@shared_task
def enviar_ganador_por_correo():
    usuarios_activos = User.objects.filter(is_active=True)
    
    if not usuarios_activos.exists():
        return "No hay usuarios activos para el sorteo."

    ganador = random.choice(usuarios_activos)
    subject = '¡Felicidades, eres el ganador del sorteo!'
    message = f'Querido/a {ganador.username}, ¡Felicidades por ser el ganador del sorteo!'
    recipient_list = [ganador.email]

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    return f'Ganador: {ganador.username}, Correo enviado a: {ganador.email}'
