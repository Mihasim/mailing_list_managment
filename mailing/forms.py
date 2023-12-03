from django import forms

from mailing.models import MailingListSettings


class MyFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(MyFormMixin, forms.ModelForm):
    class Meta:
        model = MailingListSettings
        exclude = ('date_last_mailing', 'author')
        widgets = {
            'mailing_start_time': forms.DateInput(attrs=dict(type='datetime-local'))
        }


class ModerMailingForm(MyFormMixin, forms.ModelForm):
    class Meta:
        model = MailingListSettings
        fields = ('status_mailing',)
