# Generated by Django 2.2.5 on 2019-09-19 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ControlToControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='название под-этапа')),
            ],
        ),
        migrations.CreateModel(
            name='ControlTop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='название этапа')),
            ],
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='название скрипта')),
                ('url', models.CharField(max_length=250, verbose_name='ссылка')),
            ],
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situation', models.CharField(max_length=250, verbose_name='ситуация')),
                ('recomended_action', models.TextField(blank=True, verbose_name='что говорим')),
                ('control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.ControlToControl')),
            ],
        ),
    ]
