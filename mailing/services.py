import smtplib
from calendar import calendar
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from django.core.mail import send_mail
from mailing.models import Logs


def check_date(mailing):
    """
    Функция для задания даты следующей отправки
    """
    current_time = datetime.now().replace(tzinfo=pytz.UTC)
    if mailing.mailing_start_time > current_time:
        mailing.date_last_mailing = mailing.mailing_start_time
        print("Следующая рассылка произойдет согласно расписания")
    else:
        if mailing.periodicity == "daily":
            mailing.date_last_mailing = mailing.mailing_start_time + timedelta(days=1)
            print("Создана ежедневная рассылка")

        if mailing.periodicity == "weekly":
            mailing.date_last_mailing = mailing.mailing_start_time + timedelta(days=7)
            print("Создана еженедельная рассылка")

        if mailing.periodicity == "monthly":
            today = datetime.today()
            month = calendar.monthrange(today.year, today.month)[1]
            mailing.date_last_mailing = current_time + timedelta(days=month)
            print("Создана ежедмесячная рассылка")

    return mailing.date_last_mailing


def send_mailing(mailing):
    """
    Функция отправки сообщений
    """
    if mailing.mailing_start_time >= mailing.end_of_mailing:
        mailing.status_mailing = 'done'
        mailing.save()
        print("Рассылка окончена")
        return
    else:
        try:
            for client in mailing.client.all():
                mailing.status_mailing = 'started'
                send_mail(
                    mailing.message.theme_of_message,
                    mailing.message.message_body,
                    settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                )
        except smtplib.SMTPException as e:

            if 'authentication failed' in str(e):
                status_try = 'failed'
                answer_post_server = 'Ошибка аутентификации в почтовом сервисе'
                Logs.objects.create(
                    last_try=mailing.date_last_mailing,
                    status_try=status_try,
                    answer_post_server=answer_post_server,
                    mailing=mailing
                )

            elif 'suspicion of SPAM' in str(e):
                status_try = 'failed'
                answer_post_server = 'Слишком много рассылок, сервис отклонил письмо'
                Logs.objects.create(
                    last_try=mailing.date_last_mailing,
                    status_try=status_try,
                    answer_post_server=answer_post_server,
                    mailing=mailing
                )

        else:
            answer_post_server = "Рассылка ушла к получателям"
            status_try = 'ok'
            Logs.objects.create(
                last_try=mailing.date_last_mailing,
                status_try=status_try,
                answer_post_server=answer_post_server,
                mailing=mailing
            )
