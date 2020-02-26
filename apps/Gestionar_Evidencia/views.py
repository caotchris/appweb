from django.shortcuts import render

from rest_framework.decorators import api_view
from .serializers import *
from .models import *

from rest_framework.generics import (CreateAPIView)
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers, viewsets, routers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.Gestionar_Infraccion.models import Infraccion_Transito
from django.contrib import messages

from base64 import b64decode
from django.core.files.base import ContentFile
import base64

#Listar evidencia de infraccion de tránsito
def listarEvidencia(request):
    if request.method == 'GET':
        id = request.GET['Infraccion_Transito']
        evidencia = MyImage.objects.all().filter(id_Evidencia=id)
        evidenciaa = MyAudio.objects.all().filter(id_Evidencia=id)
        evidenciav = MyVideo.objects.all().filter(id_Evidencia=id)
    # print(evidencia)
    context = {'evidencia': evidencia,
               'evidenciaa': evidenciaa,
               'evidenciav': evidenciav}
    return render(request, 'Gestion_Evidencia/verMultimedia.html', context)

# Lista evidencia de accidente
def listarEvidenciaa(request):
    if request.method == 'GET':
        id = request.GET['Accidente_Transito']
        evidencia = MyImage.objects.all().filter(id_Evidencia=id)
        evidenciaa = MyAudio.objects.all().filter(id_Evidencia=id)
        evidenciav = MyVideo.objects.all().filter(id_Evidencia=id)
    # print(evidencia)
    context = {'evidencia': evidencia,
               'evidenciaa': evidenciaa,
               'evidenciav': evidenciav}
    return render(request, 'Gestion_Evidencia/verMultimedia.html', context)


class ImageCreateAPIView(CreateAPIView):
    serializer_class = imageSerializer
    queryset = MyImage.objects.all()


class VideoCreateAPIView(CreateAPIView):
    serializer_class = videoSerializer
    queryset = MyVideo.objects.all()


class AudioCreateAPIView(CreateAPIView):
    serializer_class = audioSerializer
    queryset = MyAudio.objects.all()
