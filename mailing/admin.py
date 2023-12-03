from django.contrib import admin

from mailing.models import MailingListSettings, Message, Logs


@admin.register(MailingListSettings)
class MailingListSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_name', 'mailing_start_time', 'periodicity', 'end_of_mailing', 'status_mailing', 'message')
    search_fields = ('mailing_name', 'mailing_time', 'periodicity', 'status_mailing',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme_of_message', 'message_body')
    search_fields = ('theme_of_message', 'message_body')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'status_try', 'answer_post_server')
    search_fields = ('last_try', 'status_try', 'answer_post_server')
