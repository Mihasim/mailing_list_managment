from random import randint

from django.conf import settings
from django.core.mail import send_mail


def generate_code():
    code = randint(100000, 999999)
    return code


def verification(activation_url, user_email):
    send_mail(
        subject='Подтверждение регистрации',
        message=f'Ссылка для подтверждения регистрации:'
                f'{activation_url}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )
