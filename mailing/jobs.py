from mailing.services import send_mailing
from mailing.models import MailingListSettings


def daily_tasks():
    mailings = MailingListSettings.objects.filter(periodicity="daily", status_mailing='started')
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def weekly_tasks():
    mailings = MailingListSettings.objects.filter(periodicity="weekly", status_mailing='started')
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def monthly_tasks():
    mailings = MailingListSettings.objects.filter(periodicity="monthly", status_mailing='started')
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)
