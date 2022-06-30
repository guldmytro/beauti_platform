# Generated by Django 4.0.5 on 2022-06-17 12:42

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
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osm_type', models.CharField(max_length=30, verbose_name='Тип')),
                ('osm_id', models.CharField(max_length=30, verbose_name='Идентификатор')),
                ('city', models.CharField(max_length=200, verbose_name='Город')),
                ('display_name', models.CharField(max_length=200, verbose_name='Город (полностью)')),
                ('boundingbox', models.CharField(max_length=500, verbose_name='Координаты')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=200, verbose_name='Область')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=200, null=True, verbose_name='ФИО')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Телефон')),
                ('street', models.CharField(blank=True, max_length=400, null=True, verbose_name='Улица')),
                ('house', models.CharField(blank=True, max_length=5, null=True, verbose_name='Дом')),
                ('flat', models.CharField(blank=True, max_length=5, null=True, verbose_name='Квартира')),
                ('photo', models.ImageField(upload_to='media/%Y/%m/%d', verbose_name='Фото профиля')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Опубликовано')),
                ('city', models.ForeignKey(blank=True, max_length=400, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.city', verbose_name='Город')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.state', verbose_name='Район'),
        ),
    ]