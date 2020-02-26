from django.db import models
from apps.Gestionar_Usuarios.models import Agente_Transito
from apps.Gestionar_Informacion.models import Conductor, Vehiculo

# Create your models here.


class Articulos_COIP(models.Model):
    Id_Articulo = models.IntegerField(primary_key=True)
    Articulo = models.TextField()
    Inciso = models.TextField()
    Numeral = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Articulos_COIP'
        verbose_name_plural = 'Articulos'

    def __int__(self):
        return self.Id_Articulo


class Infraccion_Transito(models.Model):
    NumeroInfraccion = models.IntegerField(primary_key=True)
    Descripcion = models.TextField()
    Ubicacion = models.TextField()
    Latitud = models.DecimalField(max_digits=30, decimal_places=20)
    Longitud = models.DecimalField(max_digits=30, decimal_places=20)
    Estado = models.CharField(max_length=20, null=True, default="Reportado")
    Fecha_Infraccion = models.DateField()
    Fecha_Registro = models.DateField(auto_now_add=True)
    Hora_Infraccion = models.TimeField()
    Hora_Detencion = models.TimeField(null=True, blank=True)
    Hora_Registro = models.TimeField(auto_now_add=True)

    # Relacion de muchos a uno
    Agente = models.ForeignKey(
        Agente_Transito, null=True, blank=True, on_delete=models.CASCADE)
    # Relacion uno a uno
    ArticuloC = models.ForeignKey(
        Articulos_COIP, null=True, blank=True, on_delete=models.CASCADE)
    # Relacion de muchos a uno
    ##id_evidencia = models.ForeignKey (Evidencia, on_delete=models.CASCADE)
    # Relacion de uno a uno
    Conductor = models.ForeignKey(
        Conductor, null=True, blank=True, on_delete=models.CASCADE)
    # Relacion de uno a uno
    Vehiculo = models.ForeignKey(
        Vehiculo, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Infraccion_Transito'
        verbose_name_plural = 'Infracciones_Transito'

    def __int__(self):
        return self.NumeroInfraccion


class Intentos(models.Model):
    Cedula = models.IntegerField()
    Latitud = models.DecimalField(max_digits=30, decimal_places=20)
    Longitud = models.DecimalField(max_digits=30, decimal_places=20)
    Ubicacion = models.TextField()
    Fecha_Intento = models.DateField()
    Hora_Intento = models.TimeField()
    Descripcion = models.TextField(null=True, blank=True)
    Accion = models.IntegerField(null=True, blank=True)
    # Relacion de muchos a uno
    Agente = models.ForeignKey(
        Agente_Transito, null=True, blank=True, on_delete=models.CASCADE)


class ContadorInfraccion(models.Model):
    CedulaAgente = models.IntegerField()
    CodigoAgente = models.IntegerField()
    ContadorAgente = models.IntegerField()

#COntenido Articulos
class ArticulosBD(models.Model):
    NumeroArticuloBD = models.IntegerField(primary_key=True)
    DescripcionBDA = models.TextField()

#COntenido INcisos
class IncisosBD(models.Model):
    NumeroIncisoBD = models.IntegerField(primary_key=True)
    DescripcionBDI = models.TextField()

#COntenido Numeral
class NumeralBD(models.Model):
    NumeroNumeralBD = models.IntegerField(primary_key=True)
    DescripcionBDN = models.TextField()
