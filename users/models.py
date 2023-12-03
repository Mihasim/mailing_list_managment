from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

import mailing

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    verification_code = models.CharField(max_length=256, verbose_name='Код верификации', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name="Пользователь активен")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return (f'{self.full_name}: {self.email}')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'set_active',
                'can blocking users'
            ),
        ]


class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email', unique=True)
    full_name = models.CharField(max_length=150, verbose_name='ФИО', unique=True)
    comment = models.CharField(max_length=150, verbose_name='комментарий', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='чей клиент')

    def __str__(self):
        return f'{self.full_name}: {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

