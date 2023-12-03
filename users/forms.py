from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from users.models import User


class UserForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = (
            'email',
            'full_name',
        )


class ModerUserForm(UserForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)
