# Generated by Django 4.0.5 on 2022-06-29 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_city_state_alter_state_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='osm_id',
            field=models.CharField(max_length=30, unique=True, verbose_name='Идентификатор'),
        ),
    ]