from django.db import models

# MODELO

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length=50, unique=True)

class ListaTalleres(models.Model):
    id_taller = models.AutoField(primary_key=True)
    nombre_taller = models.CharField(max_length=50)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nombre_taller', 'comuna')

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.BigIntegerField()
    dv = models.CharField(max_length=1)
    direccion = models.CharField(max_length=50)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

    class Meta:
        unique_together = ('rut', 'dv')

class Agendamiento(models.Model):
    id_agendamiento = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    taller = models.ForeignKey(ListaTalleres, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agendado = models.BooleanField(default=True)
    cancelado = models.BooleanField(default=False)

class Feriados(models.Model):
    id_feriado = models.AutoField(primary_key=True)
    fecha = models.DateField()
    anio = models.IntegerField()
    descripcion = models.CharField(max_length=75)

    class Meta:
        unique_together = ('fecha', 'anio')