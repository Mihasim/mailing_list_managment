from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, \
    MessageDeleteView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, \
    LogsListView, LogsDetailView, LogsDeleteView, MainView

app_name = MailingConfig.name


urlpatterns = [
    path('', MainView.as_view(), name='index'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing_detail<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),

    path('mailing_logs_list/', LogsListView.as_view(), name='mailing_logs_list'),
    path('mailing_logs_detail/<int:pk>', LogsDetailView.as_view(), name='mailing_logs_detail'),
    path('mailing_logs_delete/<int:pk>', LogsDeleteView.as_view(), name='mailing_logs_delete'),

]
