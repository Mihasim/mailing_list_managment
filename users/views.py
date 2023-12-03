from smtplib import SMTPException

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView

from users.forms import UserForm, ModerUserForm
from users.models import Client, User
from users.services import generate_code, verification


class RegisterView(CreateView):
    """
    Контроллер для регистрации пользователя
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Метод получения данных формы"""
        secret_code = generate_code()
        user = form.save()  # Получаем данные пользователя
        user.verification_code = secret_code  # Создаем код для верификации и присваиваем пользователю
        verification_code = str(secret_code) + str(user.pk)  # К коду для верификации добавляем первичный ключ пользователя
        # Создаем ссылку для подтверждения почты
        activation_url = self.request.build_absolute_uri(
            reverse_lazy(
                'users:email_verified', kwargs={
                    'verification_code': verification_code
                }
            )
        )
        try:
            # Пробуем отправить письмо на почту
            verification(activation_url, user.email)
            user.save()
            return redirect('users:verify_send')
        except SMTPException as e:
            user.delete()
            return redirect('users:error_page')


class EmailConfirmationSentView(TemplateView):
    """Контроллер вывода страницы уведомления об отправке письма"""
    template_name = 'users/verify_send.html'


class EmailConfirmedView(TemplateView):
    """Контроллер вывода страницы подтвреждения регистрации"""
    template_name = 'users/email_verified.html'


class FailedView(TemplateView):
    """Контроллер вывода страницы подтвреждения регистрации"""
    template_name = 'users/error_page.html'


class UserConfirmEmailView(View):
    """Контрллер подтверждения регистрации по ссылке"""
    def get(self, request, verification_code):
        """Метод проверки валидность ссылки потдверждения регистрации"""
        uid = int(verification_code[6:])
        print(uid)
        code = verification_code[:6]
        print(code)
        try:
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and code == user.verification_code:
            user.is_active = True
            user.verification_code = ""
            user.save()
            return redirect(reverse_lazy('users:email_verified'))
        else:
            return redirect(reverse_lazy('users:error_page'))


class UserFormView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:user_form')
    fields = 'email', 'full_name'

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список пользователей'
        return context

    def get_queryset(self):
        """
        Вывод значений для текущего пользователя
        """
        if not self.request.user.is_staff:
            return super().get_queryset().filter(author=self.request.user)
        return super().get_queryset()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'mailing.change_user'

    def get_success_url(self):
        return reverse('mailing:user_list')



class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    permission_required = 'mailing.change_user'
    success_url = reverse_lazy('users:user_list')

    def has_permission(self):
        if self.request.user.is_staff:
            return True
        return super().has_permission()

    def get_form_class(self):
        if self.request.user.is_staff and not self.request.user.is_superuser:
            return ModerUserForm
        return UserForm


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список клиентов'
        return context

    def get_queryset(self):
        """
        Вывод значений для текущего пользователя
        """
        if not self.request.user.is_staff:
            return super().get_queryset().filter(author=self.request.user)
        return super().get_queryset()


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    success_url = reverse_lazy('users:client_list')

    def form_valid(self, form):
        Client = form.save()
        Client.owner = self.request.user
        Client.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('users:client_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    success_url = reverse_lazy('users:client_list')
