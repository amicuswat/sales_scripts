from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class ScriptsUser(AbstractUser):
    phone = models.CharField(verbose_name='телефон', max_length=30)
    company_name = models.CharField(verbose_name='компания', max_length=50)
    position =  models.CharField(verbose_name='должность', max_length=50)
    date_last_visit = models.DateTimeField(auto_now=True)
    scripts_days = models.PositiveIntegerField(verbose_name='оплачено скриптов', default=0)
    scripts_used = models.PositiveIntegerField(verbose_name='используется скриптов', default=0)


