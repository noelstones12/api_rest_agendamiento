# Generated by Django 5.0.6 on 2024-06-26 04:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id_comuna', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_comuna', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('rut', models.BigIntegerField()),
                ('dv', models.CharField(max_length=1)),
                ('direccion', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=20)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.comuna')),
            ],
            options={
                'unique_together': {('rut', 'dv')},
            },
        ),
        migrations.CreateModel(
            name='Feriados',
            fields=[
                ('id_feriado', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('anio', models.IntegerField()),
                ('descripcion', models.CharField(max_length=75)),
            ],
            options={
                'unique_together': {('fecha', 'anio')},
            },
        ),
        migrations.CreateModel(
            name='ListaTalleres',
            fields=[
                ('id_taller', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_taller', models.CharField(max_length=50)),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.comuna')),
            ],
            options={
                'unique_together': {('nombre_taller', 'comuna')},
            },
        ),
        migrations.CreateModel(
            name='Agendamiento',
            fields=[
                ('id_agendamiento', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('agendado', models.BooleanField(default=True)),
                ('cancelado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cliente')),
                ('taller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.listatalleres')),
            ],
        ),
    ]
