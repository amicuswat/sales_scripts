# Generated by Django 2.2.5 on 2019-09-27 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_auto_20190926_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SituationLinear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situation', models.CharField(max_length=250, verbose_name='ситуация')),
                ('recomended_action', models.TextField(blank=True, verbose_name='что говорим')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='позиция')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.Script')),
            ],
        ),
        migrations.CreateModel(
            name='Situation2D',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situation', models.CharField(max_length=250, verbose_name='ситуация')),
                ('recomended_action', models.TextField(blank=True, verbose_name='что говорим')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='позиция')),
                ('control_top', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.ControlTop')),
            ],
        ),
    ]
