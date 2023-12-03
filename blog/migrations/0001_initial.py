# Generated by Django 4.2.7 on 2023-12-03 12:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blogs/', verbose_name='Изображение')),
                ('views_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2023, 12, 3, 15, 18, 33, 377540), verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
