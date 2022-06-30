from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class State(models.Model):
    state = models.CharField(max_length=200, verbose_name='Область',
                             unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.state


class City(models.Model):
    osm_type = models.CharField(max_length=30, verbose_name='Тип')
    osm_id = models.CharField(max_length=30, verbose_name='Идентификатор',
                              unique=True)
    city = models.CharField(max_length=200, verbose_name='Город')
    display_name = models.CharField(max_length=200,
                                    verbose_name='Город (полностью)')
    boundingbox = models.CharField(max_length=500, verbose_name='Координаты')
    lat = models.TextField(max_length=30)
    lon = models.TextField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE,
                               verbose_name='Район', blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.city


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    fullname = models.CharField(max_length=200, verbose_name='ФИО', blank=True,
                                null=True)
    phone = models.CharField(max_length=30, verbose_name='Телефон', blank=True,
                             null=True, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             max_length=400, verbose_name='Город', blank=True,
                             null=True)
    address = models.CharField(max_length=400, verbose_name='Адрес', blank=True,
                              null=True)
    address_type = models.CharField(max_length=30, verbose_name='Тип',
                                    blank=True, null=True)
    address_id = models.CharField(max_length=30, verbose_name='Id Адреса',
                                  blank=True, null=True)
    boundingbox = models.CharField(max_length=500, verbose_name='Координаты',
                                   blank=True, null=True)
    lat = models.TextField(max_length=30, blank=True, null=True)
    lon = models.TextField(max_length=30, blank=True, null=True)
    photo = models.ImageField(verbose_name='Фото профиля',
                              upload_to='media/%Y/%m/%d', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    publish = models.DateTimeField(default=timezone.now,
                                   verbose_name='Опубликовано')

    objects = models.Manager()

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
