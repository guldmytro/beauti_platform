# Generated by Django 4.0.5 on 2022-06-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_profile_flat_remove_profile_house_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/%Y/%m/%d', verbose_name='Фото профиля'),
        ),
    ]