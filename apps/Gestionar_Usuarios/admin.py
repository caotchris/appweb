from django.contrib import admin
from .models import Agente_Transito, Juez, Administrador, NumeroInfraccion

admin.site.register(Agente_Transito)
admin.site.register(Juez)
admin.site.register(Administrador)
admin.site.register(NumeroInfraccion)
