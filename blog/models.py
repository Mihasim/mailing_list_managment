import datetime

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='blogs/', verbose_name='Изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    creation_date = models.DateTimeField(verbose_name='Дата создания', default=datetime.datetime.now())


    def __str__(self):
        return f'{self.title}'


    class Meta:
        verbose_name = ('Блог')
        verbose_name_plural = ('Блоги')