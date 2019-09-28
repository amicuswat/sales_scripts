from django.db import models

# Create your models here.
from authapp.models import ScriptsUser
from django.utils import timezone


class Transaction(models.Model):
    user = models.ForeignKey(ScriptsUser, on_delete=models.CASCADE)
    sd_burned = models.PositiveIntegerField(verbose_name='потрачено с/д', default=0)
    date_created = models.DateTimeField(verbose_name='дата тарнзакции', default=timezone.now)

class Purchase(models.Model):
    user = models.ForeignKey(ScriptsUser, on_delete=models.CASCADE)
    sd_bought = models.PositiveIntegerField(verbose_name='куплено с/д', default=0)
    rubles_payed = models.PositiveIntegerField(verbose_name='куплено с/д', default=0)
    date_created = models.DateTimeField(verbose_name='дата тарнзакции', default=timezone.now)

class InvoiceRequest(models.Model):
    user = models.ForeignKey(ScriptsUser, on_delete=models.CASCADE)
    price_per_sd = models.PositiveIntegerField(verbose_name='за 1 сд', default=10)
    quantity_sd = models.PositiveIntegerField(verbose_name='кол-во сд', default=1)
    to_pay = models.PositiveIntegerField(verbose_name='сумма', default=10)
    is_processed = models.BooleanField(verbose_name='проведен', default=False)
    comment = models.TextField(verbose_name='коментарий', blank=True)
    date_created = models.DateTimeField(verbose_name='дата заказа', default=timezone.now)
    date_processed = models.DateTimeField(verbose_name='дата проведения', null=True, blank=True)
