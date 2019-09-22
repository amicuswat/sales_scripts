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
