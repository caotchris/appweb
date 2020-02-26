from django.db import models
from apps.Gestionar_Usuarios.models import Agente_Transito
# from apps.Gestionar_Usuarios.models import Agente_Transito
# from apps.Gestionar_Evidencia.models import Evidencia
# from django.utils.timezone import timezone
#from apps.Gestionar_Infraccion.models import Infraccion_Transito


class Accidente_Transito(models.Model):
    NumeroAccidente = models.IntegerField(primary_key=True)
    TipoAccidente = models.TextField()
    Descripcion = models.TextField()
    Ubicacion = models.TextField()
    Latitud = models.DecimalField(max_digits=30, decimal_places=20)
    Longitud = models.DecimalField(max_digits=30, decimal_places=20)
    Estado = models.CharField(max_length=12, null=True)
    Fecha = models.DateField()
    Hora_Registro = models.TimeField()
    Hora_Accidente = models.TimeField()
    # Relacion de muchos a uno
    Agente = models.ForeignKey(
        Agente_Transito, null=True, blank=True, on_delete=models.CASCADE)
    # #Relacion de muchos a uno
    # evidencia_id = models.ForeignKey (Evidencia, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Accidente_Transito'
        verbose_name_plural = 'Accidentes_Transito'

    def __int__(self):
        return self.NumeroAccidente


class ContadorAccidente(models.Model):
    CedulaAgente = models.IntegerField()
    CodigoAgente = models.IntegerField()
    ContadorAgente = models.IntegerField()