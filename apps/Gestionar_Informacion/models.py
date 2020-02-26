from django.db import models
#from apps.Gestionar_Infraccion.models import Infraccion_Transito


class Conductor(models.Model):
    CedulaC = models.CharField(max_length=11, primary_key=True)
    Nombres = models.CharField(max_length=200)
    Apellidos = models.CharField(max_length=200)
    TipoLicencia = models.CharField(max_length=20)
    CategoriaLicencia = models.CharField(max_length=20)
    FechaEmisionLicencia = models.DateField()
    FechaCaducidadLicencia = models.DateField()
    Puntos = models.IntegerField(null=True, blank=True)


class Vehiculo(models.Model):
    Placa = models.CharField(max_length=10, primary_key=True)
    Marca = models.CharField(max_length=20)
    Tipo = models.CharField(max_length=20)
    Color = models.CharField(max_length=20)
    FechaMatricula = models.DateField()
    FechaCaducidadMatricula = models.DateField()