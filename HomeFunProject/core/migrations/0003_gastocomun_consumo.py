# Generated by Django 3.1.2 on 2024-11-09 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20241109_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='gastocomun',
            name='consumo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total'),
        ),
    ]