from django.db import models

# Create your models here.
from authapp.models import ScriptsUser


class Script(models.Model):
    user = models.ForeignKey(ScriptsUser, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='название скрипта', max_length=250)
    url = models.CharField(verbose_name='ссылка', max_length=250)
    is_active = models.BooleanField(verbose_name='активирован', default=False)
    last_modified = models.DateTimeField(auto_now=True)

class ControlTop(models.Model):
    name = models.CharField(verbose_name='название этапа', max_length=128)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)

class ControlToControl(models.Model):
    name = models.CharField(verbose_name='название под-этапа', max_length=128)
    control = models.ForeignKey(ControlTop, on_delete=models.CASCADE)

class Situation(models.Model):
    situation = models.CharField(verbose_name='ситуация', max_length=250)
    recomended_action = models.TextField(verbose_name='что говорим', blank=True)
    control = models.ForeignKey(ControlToControl, on_delete=models.CASCADE)
    # control_top = models.ForeignKey(ControlTop, on_delete=models.CASCADE)
    # script = models.ForeignKey(Script, on_delete=models.CASCADE)

class ActivationSlot(models.Model):
    user = models.ForeignKey(ScriptsUser, on_delete=models.CASCADE)
    script = models.PositiveIntegerField(verbose_name='ид скрипта', default=0)
    is_used = models.BooleanField(verbose_name='скрипт подключен', default=False)
    last_activation = models.DateTimeField(auto_now=True)
    duration_period = models.PositiveIntegerField(verbose_name='дней активации', default=0)