# Generated by Django 3.1.2 on 2024-11-22 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20241110_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastocomun',
            name='consumo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Consumo'),
        ),
        migrations.AlterField(
            model_name='gastocomun',
            name='total',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total'),
        ),
    ]
