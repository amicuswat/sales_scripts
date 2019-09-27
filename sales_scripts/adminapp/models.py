from django.db import models

# Create your models here.
from authapp.models import ScriptsUser


class Script(models.Model):
    user = models.ForeignKey(ScriptsUser, on_delete=models.CASCADE, related_name='+')
    description = models.TextField(verbose_name='инструкции для сейлзов', blank=True)
    name = models.CharField(verbose_name='название скрипта', max_length=250)
    url = models.CharField(verbose_name='ссылка', max_length=250)
    type = models.PositiveSmallIntegerField(verbose_name='тип', default=3)
    is_active = models.BooleanField(verbose_name='активирован', default=False)
    is_deleted = models.BooleanField(verbose_name='удален', default=False)
    last_modified = models.DateTimeField(auto_now=True)

class ControlTop(models.Model):
    name = models.CharField(verbose_name='название этапа', max_length=128)
    position = models.PositiveSmallIntegerField(verbose_name='позиция', default=0)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)

class ControlToControl(models.Model):
    name = models.CharField(verbose_name='название под-этапа', max_length=128)
    position = models.PositiveSmallIntegerField(verbose_name='позиция', default=0)
    control = models.ForeignKey(ControlTop, on_delete=models.CASCADE)

class Situation(models.Model):
    situation = models.CharField(verbose_name='ситуация', max_length=250)
    recomended_action = models.TextField(verbose_name='что говорим', blank=True)
    position = models.PositiveSmallIntegerField(verbose_name='позиция', default=0)
    control = models.ForeignKey(ControlToControl, on_delete=models.CASCADE)
    # control_top = models.ForeignKey(ControlTop, on_delete=models.CASCADE)
    # script = models.ForeignKey(Script, on_delete=models.CASCADE)

class Situation2D(models.Model):
    situation = models.CharField(verbose_name='ситуация', max_length=250)
    recomended_action = models.TextField(verbose_name='что говорим', blank=True)
    position = models.PositiveSmallIntegerField(verbose_name='позиция', default=0)
    control_top = models.ForeignKey(ControlTop, on_delete=models.CASCADE)
    # script = models.ForeignKey(Script, on_delete=models.CASCADE)

class SituationLinear(models.Model):
    situation = models.CharField(verbose_name='ситуация', max_length=250)
    recomended_action = models.TextField(verbose_name='что говорим', blank=True)
    position = models.PositiveSmallIntegerField(verbose_name='позиция', default=0)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)
