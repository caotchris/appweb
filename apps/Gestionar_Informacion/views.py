from django.shortcuts import render
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conductor, Vehiculo
from .serializers import ConductorSerializer, VehiculoSerializer
from django.contrib import messages
from apps.Gestionar_Usuarios.models import Agente_Transito


class ConductorList(generics.ListCreateAPIView):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)


class VehiculoList(generics.ListCreateAPIView):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)


def buscar_vehiculos(request):
    if request.method == 'POST':
        numeroPlaca = request.POST.get('Placa')
        if (str(numeroPlaca) != ''):
            try:
                vehiculo = Vehiculo.objects.all().filter(Placa=numeroPlaca)
                context = {
                    'vehiculo': vehiculo
                }
                return render(request, 'Gestion_Vehiculos/consulta_vehiculos.html', context)
            except Exception as e:
                messages.warning(request, "Vehiculo no encontrado")
                return render(request, 'Gestion_Vehiculos/consulta_vehiculos.html')
        else:
            messages.warning(request, "Ingrese placa a buscar")
            return render(request, 'Gestion_Vehiculos/consulta_vehiculos.html')
    else:
        return render(request, 'Gestion_Vehiculos/consulta_vehiculos.html')


def buscar_conductor(request):
    if request.method == 'POST':
        numeroCedula = request.POST.get('Cedula')
        if (str(numeroCedula) != ''):
            try:
                conductor = Conductor.objects.all().filter(CedulaC=numeroCedula)
                context = {
                    'conductor': conductor
                }
                return render(request, 'Gestion_Conductor/consulta_conductor.html', context)
            except Exception as e:
                messages.warning(request, "Conductor no encontrado")
                return render(request, 'Gestion_Conductor/consulta_conductor.html')
        else:
            messages.warning(request, "Ingrese placa a buscar")
            return render(request, 'Gestion_Conductor/consulta_conductor.html')
    else:
        return render(request, 'Gestion_Conductor/consulta_conductor.html')


def buscar_agente(request):
    if request.method == 'POST':
        numeroCedula = request.POST.get('Cedula')

        if (str(numeroCedula) != ''):
            try:
                agente = Agente_Transito.objects.all().filter(Cedula=numeroCedula)
                context = {
                    'agente': agente
                }

                return render(request, 'Gestion_Agente/buscar_agente.html', context)
            except Exception as e:
                messages.warning(request, "Agente no encontrado")
                return render(request, 'Gestion_Agente/buscar_agente.html')
        else:
            messages.warning(request, "Ingrese Cedula a buscar")
            return render(request, 'Gestion_Agente/buscar_agente.html')
    else:
        return render(request, 'Gestion_Agente/buscar_agente.html')
