from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from users.models import Client

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    theme_of_message = models.CharField(max_length=150, verbose_name='тема письма',  unique=True)
    message_body = models.TextField(verbose_name='тело сообщения')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Создатель сообщения')

    def __str__(self):
        return f'{self.theme_of_message}: {self.message_body}'

    class Meta:
        verbose_name = 'сообщение для рассылки'
        verbose_name_plural = 'сообщения для рассылки'


class MailingListSettings(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = [
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Еженедельная'),
        (PERIOD_MONTHLY, 'Ежемесячная'),
    ]

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена'),
    ]

    mailing_name = models.CharField(max_length=50, verbose_name='название рассылки',  unique=True)
    creation_date = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    mailing_start_time = models.DateTimeField(verbose_name='Дата начала рассылки', **NULLABLE)
    date_last_mailing = models.DateTimeField(verbose_name='Дата следующей отправки', **NULLABLE)
    periodicity = models.CharField(max_length=20, verbose_name='периодичность', choices=PERIODS)
    end_of_mailing = models.DateTimeField(default=datetime.now() + timedelta(days=365), verbose_name='дата и время окончания рассылки')
    status_mailing = models.CharField(max_length=50, verbose_name='статус рассылки', choices=STATUSES)
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name='текст рассылки')
    client = models.ManyToManyField(Client, verbose_name='Клиент для рассылки', related_name='clients')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Создатель рассылки')


    def __str__(self):
        return f'{self.periodicity}, {self.status_mailing}'

    class Meta:
        verbose_name = 'рассылка (настройки)'
        verbose_name_plural = 'рассылки (настройки)'
        permissions = [
            (
                'set_status_mailing',
                'can off mailing'
            ),
        ]


class Logs(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = [
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    ]

    last_try = models.DateTimeField(verbose_name='Дата и время последней попытки')
    status_try = models.CharField(max_length=20, verbose_name='статус попытки',  choices=STATUSES)
    answer_post_server = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(MailingListSettings, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f'{self.last_try}: {self.status_try} {self.answer_post_server}'

    class Meta:
        verbose_name = 'лог рассылки'
        verbose_name_plural = 'логи рассылки'
