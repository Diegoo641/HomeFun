# Generated by Django 3.1.2 on 2024-11-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_tipogastocomun_medida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipogastocomun',
            name='medida',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Medida'),
        ),
    ]
