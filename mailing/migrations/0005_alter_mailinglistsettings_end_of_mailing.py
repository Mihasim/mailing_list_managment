# Generated by Django 4.2.7 on 2023-12-03 08:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_message_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglistsettings',
            name='end_of_mailing',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 2, 11, 26, 5, 865644), verbose_name='дата и время окончания рассылки'),
        ),
    ]
