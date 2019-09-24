# Generated by Django 2.2.5 on 2019-09-24 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sd_burned', models.PositiveIntegerField(default=0, verbose_name='потрачено с/д')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата тарнзакции')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sd_bought', models.PositiveIntegerField(default=0, verbose_name='куплено с/д')),
                ('rubles_payed', models.PositiveIntegerField(default=0, verbose_name='куплено с/д')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата тарнзакции')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
