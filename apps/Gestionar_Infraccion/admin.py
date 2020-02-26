from django.contrib import admin
from .models import Infraccion_Transito, Articulos_COIP, Intentos, ContadorInfraccion, ArticulosBD, IncisosBD, NumeralBD

admin.site.register(Infraccion_Transito)
admin.site.register(Articulos_COIP)
admin.site.register(Intentos)
admin.site.register(ContadorInfraccion)
admin.site.register(ArticulosBD)
admin.site.register(IncisosBD)
admin.site.register(NumeralBD)
