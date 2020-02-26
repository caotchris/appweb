from django.db import models
#from apps.Gestionar_Infraccion.models import Infraccion_Transito
# from apps.Gestionar_Accidente.models import Accidente_Transito


class Agente_Transito(models.Model):
    Cedula = models.IntegerField(primary_key=True)
    Codigo_Agente = models.IntegerField()
    Nombres = models.CharField(max_length=30)
    Apellidos = models.CharField(max_length=30)
    Clave = models.CharField(max_length=20)
    fotoA = models.FileField(upload_to='imagenes/', blank=True, null=True)

    class Meta:
        verbose_name = 'Agente_Transito'
        verbose_name_plural = 'Agente de transito'

    def __int__(self):
        return self.Codigo


class Juez(models.Model):
    Cedula = models.IntegerField(primary_key=True)
    Codigo_Juez = models.IntegerField()
    Nombres = models.CharField(max_length=30)
    Apellidos = models.CharField(max_length=30)
    Clave = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Juez'
        verbose_name_plural = 'Juez'

    def __int__(self):
        return self.Codigo


class Administrador(models.Model):
    Cedula = models.IntegerField(primary_key=True)
    Codigo_Admin = models.IntegerField()
    Nombres = models.CharField(max_length=30)
    Apellidos = models.CharField(max_length=30)
    Clave = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administrador'

    def __int__(self):
        return self.Codigo


class NumeroInfraccion(models.Model):
    Id_numeroInfraccion = models.AutoField(primary_key=True)
    NumeroInfraccion = models.IntegerField()
    Codigo_Agente = models.IntegerField()
