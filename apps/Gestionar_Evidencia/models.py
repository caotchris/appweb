
from django.db import models

class MyImage(models.Model):
    model_pic = models.FileField(upload_to='imagenes/', blank=True, null=True)
    # Es igual all numero de infraccion de infraccion registrada
    id_Evidencia = models.CharField(max_length=100, null=True, blank=True)


class MyVideo(models.Model):
    model_vid = models.FileField(upload_to='videos/', blank=True, null=True)
    # Es igual all numero de infraccion de infraccion registrada
    id_Evidencia = models.CharField(max_length=100, null=True, blank=True)


class MyAudio(models.Model):
    model_aud = models.FileField(upload_to='audio/', blank=True, null=True)
    # Es igual all numero de infraccion de infraccion registrada
    id_Evidencia = models.CharField(max_length=100, null=True, blank=True)
