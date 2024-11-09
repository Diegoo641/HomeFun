# Generated by Django 3.1.2 on 2024-11-09 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado_residente',
            fields=[
                ('id_est_r', models.AutoField(primary_key=True, serialize=False, verbose_name='ID de Estado del residente')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción del Estado')),
            ],
        ),
        migrations.AddField(
            model_name='ficharesidente',
            name='estado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.estado_residente', verbose_name='Estado del residente'),
        ),
    ]
