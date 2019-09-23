from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class ScriptsUser(AbstractUser):
    phone = models.CharField(verbose_name='телефон', max_length=30)
    company_name = models.CharField(verbose_name='компания', max_length=50)
    position = models.CharField(verbose_name='должность', max_length=50)
    date_last_visit = models.DateTimeField(auto_now=True)
    captain_id = models.PositiveIntegerField(verbose_name='имя капитана', default=0)
    scripts_days = models.PositiveIntegerField(verbose_name='оплачено скриптов', default=0)
    scripts_used = models.PositiveIntegerField(verbose_name='используется скриптов', default=0)

class UserRights(models.Model):
    user = models.ForeignKey(ScriptsUser, on_delete=models.CASCADE)
    can_edit_scripts = models.BooleanField(verbose_name='редактирует скрипты', default=True)
    can_buy_sd = models.BooleanField(verbose_name='покупает СД', default=True)
    can_edit_users = models.BooleanField(verbose_name='меняет пользователей', default=True)
    can_activate_scripts = models.BooleanField(verbose_name='запускает скрипты', default=True)


