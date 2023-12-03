import random

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from mailing.forms import MailingForm, ModerMailingForm
from mailing.models import Message, MailingListSettings, Logs
from mailing.services import send_mailing, check_date
from users.models import Client


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ('theme_of_message', 'message_body')
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        Message = form.save()
        Message.author = self.request.user
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    permission_required = 'massage.delete_messege'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    permission_required = 'massage.cange_messege'
    fields = ('theme_of_message', 'message_body')
    success_url = reverse_lazy('mailing:message_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список сообщеий'
        return context

    def get_queryset(self):
        """
        Вывод значений для текущего пользователя
        """
        if not self.request.user.is_staff:
            return super().get_queryset().filter(author=self.request.user)
        return super().get_queryset()


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingListSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список рассылок'
        return context

    def get_queryset(self):
        """
        Вывод значений для текущего пользователя
        """
        if not self.request.user.is_staff:
            return super().get_queryset().filter(author=self.request.user)
        return super().get_queryset()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingListSettings
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        mailing.author = self.request.user
        mailing.date_last_mailing = check_date(mailing)
        mailing.status_mailing = 'created'
        mailing.save()
        send_mailing(mailing)
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = MailingListSettings
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingListSettings
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.delete_mailing'


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingListSettings
    form_class = MailingForm
    permission_required = 'mailing.change_mailing'

    def get_success_url(self):
        return reverse('mailing:mailing_list')

    def has_permission(self):
        object = self.get_object()
        if self.request.user == object.author or self.request.user.is_staff:
            return True
        return super().has_permission()

    def get_form_class(self):
        if self.request.user.is_staff and not self.request.user.is_superuser:
            return ModerMailingForm
        return MailingForm


class LogsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "mailing.view_logs"
    model = Logs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список логов'
        return context


class LogsDetailView(LoginRequiredMixin, DetailView):
    model = Logs


class LogsDeleteView(LoginRequiredMixin, DeleteView):
    model = Logs
    success_url = reverse_lazy('mailing:mailing_logs_list')


class MainView(TemplateView):
    """
    вывод главной страницы
    """
    template_name = 'mailing/index.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        if self.request.method == 'GET':
            if settings.CACHE_ENABLED:
                key = f'cached_statistics'
                cached_context = cache.get(key)

                if cached_context is None:
                    context_data = super().get_context_data(**kwargs)
                    if not user.is_staff:
                        context_data['mailing_count'] = MailingListSettings.objects.filter(author=user).count()
                        context_data['started_mailing_count'] = MailingListSettings.objects.filter(author=user).filter(status_mailing='started').count()
                        context_data['users_count'] = Client.objects.filter(owner=user).distinct('email').count()
                    else:
                        context_data['mailing_count'] = MailingListSettings.objects.all().count()
                        context_data['started_mailing_count'] = MailingListSettings.objects.all().filter(status_mailing='started').count()
                        context_data['users_count'] = Client.objects.all().distinct('email').count()
                        main_page_context = {
                            'mailing_count': context_data['mailing_count'],
                            'started_mailing_count': context_data['started_mailing_count'],
                            'users_count': context_data['users_count']
                        }
                        cache.set(key, main_page_context)
                        all_blog_posts = Blog.objects.all()
                        random_posts = random.sample(list(all_blog_posts), 3)
                        context_data['random_posts'] = random_posts
                    return context_data
                else:
                    context_data = super().get_context_data(*args, **kwargs)
                    context_data['mailing_count'] = cached_context['mailing_count']
                    context_data['started_mailing_count'] = cached_context['started_mailing_count']
                    context_data['users_count'] = cached_context['users_count']
                    all_blog_posts = Blog.objects.all()
                    random_posts = random.sample(list(all_blog_posts), 3)
                    context_data['random_posts'] = random_posts
                return context_data
