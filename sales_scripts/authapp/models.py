from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class ScriptsUser(AbstractUser):
    date_last_visit = models.DateTimeField(auto_now=True)
    scripts_days = models.PositiveIntegerField(verbose_name='оплачено скриптов', default=0)
    scripts_used = models.PositiveIntegerField(verbose_name='используется скриптов', default=0)


