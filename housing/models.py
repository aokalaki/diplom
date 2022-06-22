from django.db import models


class Advertisement(models.Model):
    address = models.CharField('адрес объекта аренды', max_length=255)
    rooms = models.PositiveIntegerField('количество комнат')
    conditions = models.CharField('бытовые условия', max_length=255)
    duration = models.PositiveIntegerField('срок сдачи')
    price = models.PositiveIntegerField('цена')
    date = models.DateField('дата подачи', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
