from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import ConductorList, VehiculoList, buscar_vehiculos, buscar_conductor, buscar_agente
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('conductor/', ConductorList.as_view(), name='conductor_list'),
    path('vehiculo/', VehiculoList.as_view(), name='vehiculo_list'),
    path('buscarVehiculo/', buscar_vehiculos, name='buscar_vehiculo'),
    path('buscarConductor/', buscar_conductor, name='buscar_conductor'),
    path('buscarAgente/', buscar_agente, name='buscar_agente_datos'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
