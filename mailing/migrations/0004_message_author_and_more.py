# Generated by Django 4.2.7 on 2023-12-03 08:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0003_mailinglistsettings_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создатель сообщения'),
        ),
        migrations.AlterField(
            model_name='mailinglistsettings',
            name='end_of_mailing',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 2, 11, 8, 57, 416980), verbose_name='дата и время окончания рассылки'),
        ),
    ]
