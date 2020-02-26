from django.shortcuts import render, redirect
from .forms import Accidente_TransitoForm
from apps.Gestionar_Evidencia.forms import imageform, videoform, audioform
from .models import Accidente_Transito
from apps.Gestionar_Evidencia.models import MyImage, MyVideo, MyAudio
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
from .serializers import AccidenteSerializer
from django.contrib import messages
import datetime


class AccidenteList(generics.ListCreateAPIView):
    queryset = Accidente_Transito.objects.all()
    serializer_class = AccidenteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)


def crearAccidente_Transito(request):

    NumeroAccidente = request.POST.get('NumeroAccidente')
    TipoAccidente = request.POST.get('TipoAccidente')
    fechaInicio = request.POST.get('FechaInicio')
    fechaFin = request.POST.get('FechaFin')

    if str(NumeroAccidente)+'' != '': 
        try:
             accidentes = Accidente_Transito.objects.filter(pk=NumeroAccidente)
             contador = Accidente_Transito.objects.filter(pk=NumeroAccidente).count()
             return render(request, 'Gestionar_Accidente/crear_accidente_transito.html', {'accidentes': accidentes, 'contador': contador})
        except Accidente_Transito.DoesNotExist:
             messages.warning(request, 'No se encontraron coincidencias')
             return render(request, 'Gestionar_Accidente/crear_accidente_transito.html')
    elif (str(fechaFin)+'' != '') & (str(fechaInicio)+'' != ''):
        try:

            if str(TipoAccidente)+'' == 'Todos':
                accidentes = Accidente_Transito.objects.all().filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin)
                contador = Accidente_Transito.objects.filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin).count()
            else:
                accidentes = Accidente_Transito.objects.all().filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin, TipoAccidente=TipoAccidente)
                contador = Accidente_Transito.objects.filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin, TipoAccidente=TipoAccidente).count()

            return render(request, 'Gestionar_Accidente/crear_accidente_transito.html', {'accidentes': accidentes, 'contador': contador})
        except Accidente_Transito.DoesNotExist:
            messages.warning(request, 'No se encontraron coincidencias')
            return render(request, 'Gestionar_Accidente/crear_accidente_transito.html')

    else:
        messages.warning(request, 'Ingrese NumeroAccidente')
        return render(request, 'Gestionar_Accidente/crear_accidente_transito.html')


def crearAccidente_Transito_juez(request):

    NumeroAccidente = request.POST.get('NumeroAccidente')
    TipoAccidente = request.POST.get('TipoAccidente')
    fechaInicio = request.POST.get('FechaInicio')
    fechaFin = request.POST.get('FechaFin')

    if str(NumeroAccidente)+'' != '':
        try:
            accidentes = Accidente_Transito.objects.filter(pk=NumeroAccidente)
            contador = Accidente_Transito.objects.filter(pk=NumeroAccidente).count()
            return render(request, 'Gestionar_Accidente/crear_accidente_transito_juez.html', {'accidentes': accidentes, 'contador': contador})
        except Accidente_Transito.DoesNotExist:
            messages.warning(request, 'No se encontraron coincidencias')
            return render(request, 'Gestionar_Accidente/crear_accidente_transito_juez.html')
    
    elif (str(fechaFin)+'' != '') & (str(fechaInicio)+'' != ''):
        try:
            
            if str(TipoAccidente)+'' == 'Todos':
                accidentes = Accidente_Transito.objects.all().filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin)
                contador = Accidente_Transito.objects.filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin).count()
            else:
                accidentes = Accidente_Transito.objects.all().filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin, TipoAccidente=TipoAccidente)
                contador = Accidente_Transito.objects.filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin, TipoAccidente=TipoAccidente).count()
            
            return render(request, 'Gestionar_Accidente/crear_accidente_transito_juez.html', {'accidentes': accidentes, 'contador': contador})
        except Accidente_Transito.DoesNotExist:
            messages.warning(request, 'No se encontraron coincidencias')
            return render(request, 'Gestionar_Accidente/crear_accidente_transito_juez.html')

    else:
        messages.warning(request, 'Ingrese NumeroAccidente')
        return render(request, 'Gestionar_Accidente/crear_accidente_transito_juez.html')


def buscarAccidente_Transito(request):
    if request.method == 'POST':
        try:
            numeroAccidente = request.POST.get('NumeroAccidente')
            # accidente = Accidente_Transito.objects.all().filter(
            #     NumeroAccidente=request.POST.get('NumeroAccidente'))
            return redirect("/Gestionar_Accidente/detalle_accidente_transito/?NumeroAccidente="+numeroAccidente)
        except Exception as e:
            accidente_transitoForm = Accidente_TransitoForm()
            messages.warning(request, 'Ingrese NumeroAccidente')
            return render(request, 'Gestionar_Accidente/buscar_accidente.html', {'accidente_transitoForm': accidente_transitoForm})

    else:
        accidente_transitoForm = Accidente_TransitoForm()
        return render(request, 'Gestionar_Accidente/buscar_accidente.html', {'accidente_transitoForm': accidente_transitoForm})


def detalleAccidente_Transito(request):
    if request.method == 'POST':
        numeroAccidente = request.POST.get('NumeroAccidente')
        try:
            accidente = Accidente_Transito.objects.get(
                NumeroAccidente=numeroAccidente)
            accidente.Estado = request.POST.get('Estado')
            accidente.save()
            messages.warning(request, 'Actualizacion correcta')
            return redirect('/Gestionar_Accidente/bucar_accidente_transito/')

        except Exception as e:
            accidente_transitoForm = Accidente_TransitoForm()
            messages.warning(request, 'Numero Incorrecto')
            return redirect('/Gestionar_Accidente/bucar_accidente_transito/')

    else:
        try:
            accidente = Accidente_Transito.objects.all().filter(
                NumeroAccidente=request.GET['NumeroAccidente'])
            accidente_transitoForm = Accidente_TransitoForm()
            contex = {
                'accidente': accidente,
                'accidente_transitoForm': accidente_transitoForm
            }
            return render(request, 'Gestionar_Accidente/formulario_accidente.html', contex)
        except Exception as e:
            messages.warning(request, 'Numero Incorrecto')
            accidente_transitoForm = Accidente_TransitoForm()
            return redirect('/Gestionar_Accidente/bucar_accidente_transito/')


def mapaAccidente(request):
    if request.method == 'GET':
        id = request.GET['Accidente_Transito']
        accidente = Accidente_Transito.objects.all().filter(NumeroAccidente=id)

    context = {'accidente': accidente,
               }
    return render(request, 'Gestionar_Accidente/mapaAccidente.html', context)


def Reportesadicionara(request):
    if request.method == 'POST':
        id = request.GET['Accidente_Transito']

        foto = MyImage()
        foto.model_pic = request.POST.get('model_pic')
        foto.id_Evidencia = request.GET['Accidente_Transito']
        if foto.model_pic != '':
            foto.model_pic = request.FILES.get('model_pic')
            foto.save()

        audio = MyAudio()
        audio.model_aud = request.POST.get('model_aud')
        audio.id_Evidencia = request.GET['Accidente_Transito']
        if audio.model_aud != '':
            audio.model_aud = request.FILES.get('model_aud')
            audio.save()

        video = MyVideo()
        video.model_vid = request.POST.get('model_vid')
        video.id_Evidencia = request.GET['Accidente_Transito']
        if video.model_vid != '':
            video.model_vid = request.FILES.get('model_vid')
            video.save()

        messages.warning(request, 'Actualizacion correcta')
        return redirect('/Gestionar_Accidente/crear_accidente_transito/')
    else:
        accidente_form = Accidente_TransitoForm()
        audform = audioform(request.POST, request.FILES)
        vidform = videoform(request.POST, request.FILES)
        fotoform = imageform(request.POST, request.FILES)
        id = request.GET['Accidente_Transito']
        accidente = Accidente_Transito.objects.all().filter(NumeroAccidente=id)
        context = {'accidente': accidente, 'accidente_form': accidente_form,
                   'audform': audform, 'vidform': vidform, 'fotoform': fotoform}
        return render(request, 'Gestionar_Accidente/reportesa.html', context)


def apinindex(request):
    try:
        id = request.GET['Accidente_Transito']
        accidente = Accidente_Transito.objects.all().filter(NumeroAccidente=id)
        context = {'accidente': accidente}
        messages.warning(request, 'Actualizacion correcta')
        return render(request, 'Gestionar_Accidente/accidentepin.html', context)

    except Exception as e:
        messages.warning(request, 'Actualizacion correcta')
        return redirect('/index/')


import io
import matplotlib
import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample

import numpy as np

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import tkinter as tk
from tkinter import ttk


def ploter2020(request):
  
    if request.method == 'POST':
        TipoAccidente = request.POST.get('TipoAccidente')
        ano = request.POST.get('Ano')
   
        #Enero
        fechaInicioe = str(ano+'-1-1')
        datese = datetime.datetime.strptime(fechaInicioe, '%Y-%m-%d').date()
        fechaFine = datese + datetime.timedelta(days=30)
        #Febrero
        fechaIniciof = str(ano+'-2-1')
        datesf = datetime.datetime.strptime(fechaIniciof, '%Y-%m-%d').date()
        fechaFinf = datesf + datetime.timedelta(days=30)
        #Marzo
        fechaIniciom = str(ano+'-3-1')
        datesm = datetime.datetime.strptime(fechaIniciom, '%Y-%m-%d').date()
        fechaFinm = datesm + datetime.timedelta(days=30)
        #abril
        fechaInicioa = str(ano+'-4-1')
        datesa = datetime.datetime.strptime(fechaInicioa, '%Y-%m-%d').date()
        fechaFina = datesa + datetime.timedelta(days=30)
        #mayo
        fechaIniciomy = str(ano+'-5-1')
        datesmy = datetime.datetime.strptime(fechaIniciomy, '%Y-%m-%d').date()
        fechaFinmy = datesmy + datetime.timedelta(days=30)
        #junio
        fechaIniciojn = str(ano+'-6-1')
        datesjn = datetime.datetime.strptime(fechaIniciojn, '%Y-%m-%d').date()
        fechaFinjn = datesjn + datetime.timedelta(days=30)
        #julio
        fechaIniciojl = str(ano+'-7-1')
        datesjl = datetime.datetime.strptime(fechaIniciojl, '%Y-%m-%d').date()
        fechaFinjl = datesjl + datetime.timedelta(days=30)
        #agosto
        fechaInicioag = str(ano+'-8-1')
        datesag = datetime.datetime.strptime(fechaInicioag, '%Y-%m-%d').date()
        fechaFinag = datesag + datetime.timedelta(days=30)
        #septiembre
        fechaInicios = str(ano+'-9-1')
        datess = datetime.datetime.strptime(fechaInicios, '%Y-%m-%d').date()
        fechaFins = datess + datetime.timedelta(days=30)
        #octubre
        fechaInicioo = str(ano+'-10-1')
        dateso = datetime.datetime.strptime(fechaInicioo, '%Y-%m-%d').date()
        fechaFino = dateso + datetime.timedelta(days=30)
        #noviembre
        fechaInicion = str(ano+'-11-1')
        datesn = datetime.datetime.strptime(fechaInicion, '%Y-%m-%d').date()
        fechaFinn = datesn + datetime.timedelta(days=30)
        #diciembre
        fechaIniciod = str(ano+'-12-1')
        datesd = datetime.datetime.strptime(fechaIniciod, '%Y-%m-%d').date()
        fechaFind = datesd + datetime.timedelta(days=30)

    
        if str(TipoAccidente)+'' == 'Todos':
            enero = Accidente_Transito.objects.filter(Fecha__gte=datese, Fecha__lte=fechaFine).count()
            febrero = Accidente_Transito.objects.filter(Fecha__gte=datesf, Fecha__lte=fechaFinf).count()
            marzo = Accidente_Transito.objects.filter(Fecha__gte=datesm, Fecha__lte=fechaFinm).count()
            abril = Accidente_Transito.objects.filter(Fecha__gte=datesa, Fecha__lte=fechaFina).count()
            mayo = Accidente_Transito.objects.filter(Fecha__gte=datesmy, Fecha__lte=fechaFinmy).count()
            junio = Accidente_Transito.objects.filter(Fecha__gte=datesjn, Fecha__lte=fechaFinjn).count()
            julio = Accidente_Transito.objects.filter(Fecha__gte=datesjl, Fecha__lte=fechaFinjl).count()
            agosto = Accidente_Transito.objects.filter(Fecha__gte=datesag, Fecha__lte=fechaFinag).count()
            septiembre = Accidente_Transito.objects.filter(Fecha__gte=datess, Fecha__lte=fechaFins).count()
            octubre = Accidente_Transito.objects.filter(Fecha__gte=dateso, Fecha__lte=fechaFino).count()
            noviembre = Accidente_Transito.objects.filter(Fecha__gte=datesn, Fecha__lte=fechaFinn).count()
            diciembre = Accidente_Transito.objects.filter(Fecha__gte=datesd, Fecha__lte=fechaFind).count()
        else:
            enero = Accidente_Transito.objects.filter(Fecha__gte=datese, Fecha__lte=fechaFine, TipoAccidente=TipoAccidente).count()
            febrero = Accidente_Transito.objects.filter(Fecha__gte=datesf, Fecha__lte=fechaFinf, TipoAccidente=TipoAccidente).count()
            marzo = Accidente_Transito.objects.filter(Fecha__gte=datesm, Fecha__lte=fechaFinm, TipoAccidente=TipoAccidente).count()
            abril = Accidente_Transito.objects.filter(Fecha__gte=datesa, Fecha__lte=fechaFina, TipoAccidente=TipoAccidente).count()
            mayo = Accidente_Transito.objects.filter(Fecha__gte=datesmy, Fecha__lte=fechaFinmy, TipoAccidente=TipoAccidente).count()
            junio = Accidente_Transito.objects.filter(Fecha__gte=datesjn, Fecha__lte=fechaFinjn, TipoAccidente=TipoAccidente).count()
            julio = Accidente_Transito.objects.filter(Fecha__gte=datesjl, Fecha__lte=fechaFinjl, TipoAccidente=TipoAccidente).count()
            agosto = Accidente_Transito.objects.filter(Fecha__gte=datesag, Fecha__lte=fechaFinag, TipoAccidente=TipoAccidente).count()
            septiembre = Accidente_Transito.objects.filter(Fecha__gte=datess, Fecha__lte=fechaFins, TipoAccidente=TipoAccidente).count()
            octubre = Accidente_Transito.objects.filter(Fecha__gte=dateso, Fecha__lte=fechaFino, TipoAccidente=TipoAccidente).count()
            noviembre = Accidente_Transito.objects.filter(Fecha__gte=datesn, Fecha__lte=fechaFinn, TipoAccidente=TipoAccidente).count()
            diciembre = Accidente_Transito.objects.filter(Fecha__gte=datesd, Fecha__lte=fechaFind, TipoAccidente=TipoAccidente).count()

        total = enero+febrero+marzo+abril+mayo+junio+julio+agosto+septiembre+octubre+noviembre+diciembre

        context = {
                    'enero': enero,
                    'febrero' : febrero,
                    'marzo' : marzo,
                    'abril' : abril,
                    'mayo' : mayo,
                    'junio' : junio,
                    'julio' : julio,
                    'agosto' : agosto,
                    'septiembre' : septiembre,
                    'octubre' : octubre,
                    'noviembre' : noviembre,
                    'diciembre' : diciembre,
                    'total': total
                }

        x = [1,2,3,4,5,6,7,8,9,10,11,12]
        y = [int(enero),int(febrero),int(marzo),int(abril),int(mayo),int(junio),int(julio),int(agosto),int(septiembre),int(octubre),int(noviembre),int(diciembre)]


        # Creamos una figura y le dibujamos el gráfico
        f = plt.figure()

        # Creamos los ejes
        axes = f.add_axes([0.15, 0.15, 0.75, 0.75]) # [left, bottom, width, height]
        axes.bar(x,y, color = "r")
        axes.plot(x,y, marker='o', linestyle=':', color='b')
        axes.set_xlabel("Meses")
        axes.set_ylabel("Accidentes")
        axes.set_title("GRAFICO ACCIDENTES"+" "+ano+" "+TipoAccidente)
        axes.grid(True)       

        # Como enviaremos la imagen en bytes la guardaremos en un buffer
        buf = io.BytesIO()
        canvas = FigureCanvasAgg(f)
        canvas.print_png(buf)

        # Creamos la respuesta enviando los bytes en tipo imagen png
        response = HttpResponse(buf.getvalue(), content_type='image/png')

        # Limpiamos la figura para liberar memoria
        f.clear()

        # Añadimos la cabecera de longitud de fichero para más estabilidad
        response['Content-Length'] = str(len(response.content))

        # Devolvemos la response
        return response

        return render(request, "Gestionar_Accidente/estadistica2020.html", context)
    else:
        return render(request, "Gestionar_Accidente/estadistica2020.html")






import csv
from django.http import HttpResponse
import django_excel as excel

def exportar_csv(request):
        ano1 = '2019'
        ano = '2020'

    #2019
        fechaInicioe1 = str(ano1+'-1-1')
        datese1 = datetime.datetime.strptime(fechaInicioe1, '%Y-%m-%d').date()
        fechaFine1 = datese1 + datetime.timedelta(days=30)
        #Febrero
        fechaIniciof1 = str(ano1+'-2-1')
        datesf1 = datetime.datetime.strptime(fechaIniciof1, '%Y-%m-%d').date()
        fechaFinf1 = datesf1 + datetime.timedelta(days=30)
        #Marzo
        fechaIniciom1 = str(ano1+'-3-1')
        datesm1 = datetime.datetime.strptime(fechaIniciom1, '%Y-%m-%d').date()
        fechaFinm1 = datesm1 + datetime.timedelta(days=30)
        #abril
        fechaInicioa1 = str(ano1+'-4-1')
        datesa1 = datetime.datetime.strptime(fechaInicioa1, '%Y-%m-%d').date()
        fechaFina1 = datesa1 + datetime.timedelta(days=30)
        #mayo
        fechaIniciomy1 = str(ano1+'-5-1')
        datesmy1 = datetime.datetime.strptime(fechaIniciomy1, '%Y-%m-%d').date()
        fechaFinmy1 = datesmy1 + datetime.timedelta(days=30)
        #junio
        fechaIniciojn1 = str(ano1+'-6-1')
        datesjn1 = datetime.datetime.strptime(fechaIniciojn1, '%Y-%m-%d').date()
        fechaFinjn1 = datesjn1 + datetime.timedelta(days=30)
        #julio
        fechaIniciojl1 = str(ano1+'-7-1')
        datesjl1 = datetime.datetime.strptime(fechaIniciojl1, '%Y-%m-%d').date()
        fechaFinjl1 = datesjl1 + datetime.timedelta(days=30)
        #agosto
        fechaInicioag1 = str(ano1+'-8-1')
        datesag1 = datetime.datetime.strptime(fechaInicioag1, '%Y-%m-%d').date()
        fechaFinag1 = datesag1 + datetime.timedelta(days=30)
        #septiembre
        fechaInicios1 = str(ano1+'-9-1')
        datess1 = datetime.datetime.strptime(fechaInicios1, '%Y-%m-%d').date()
        fechaFins1 = datess1 + datetime.timedelta(days=30)
        #octubre
        fechaInicioo1 = str(ano1+'-10-1')
        dateso1 = datetime.datetime.strptime(fechaInicioo1, '%Y-%m-%d').date()
        fechaFino1 = dateso1 + datetime.timedelta(days=30)
        #noviembre
        fechaInicion1 = str(ano1+'-11-1')
        datesn1 = datetime.datetime.strptime(fechaInicion1, '%Y-%m-%d').date()
        fechaFinn1 = datesn1 + datetime.timedelta(days=30)
        #diciembre
        fechaIniciod1 = str(ano1+'-12-1')
        datesd1 = datetime.datetime.strptime(fechaIniciod1, '%Y-%m-%d').date()
        fechaFind1 = datesd1 + datetime.timedelta(days=30)

#2020
        fechaInicioe = str(ano+'-1-1')
        datese = datetime.datetime.strptime(fechaInicioe, '%Y-%m-%d').date()
        fechaFine = datese + datetime.timedelta(days=30)
        #Febrero
        fechaIniciof = str(ano+'-2-1')
        datesf = datetime.datetime.strptime(fechaIniciof, '%Y-%m-%d').date()
        fechaFinf = datesf + datetime.timedelta(days=30)
        #Marzo
        fechaIniciom = str(ano+'-3-1')
        datesm = datetime.datetime.strptime(fechaIniciom, '%Y-%m-%d').date()
        fechaFinm = datesm + datetime.timedelta(days=30)
        #abril
        fechaInicioa = str(ano+'-4-1')
        datesa = datetime.datetime.strptime(fechaInicioa, '%Y-%m-%d').date()
        fechaFina = datesa + datetime.timedelta(days=30)
        #mayo
        fechaIniciomy = str(ano+'-5-1')
        datesmy = datetime.datetime.strptime(fechaIniciomy, '%Y-%m-%d').date()
        fechaFinmy = datesmy + datetime.timedelta(days=30)
        #junio
        fechaIniciojn = str(ano+'-6-1')
        datesjn = datetime.datetime.strptime(fechaIniciojn, '%Y-%m-%d').date()
        fechaFinjn = datesjn + datetime.timedelta(days=30)
        #julio
        fechaIniciojl = str(ano+'-7-1')
        datesjl = datetime.datetime.strptime(fechaIniciojl, '%Y-%m-%d').date()
        fechaFinjl = datesjl + datetime.timedelta(days=30)
        #agosto
        fechaInicioag = str(ano+'-8-1')
        datesag = datetime.datetime.strptime(fechaInicioag, '%Y-%m-%d').date()
        fechaFinag = datesag + datetime.timedelta(days=30)
        #septiembre
        fechaInicios = str(ano+'-9-1')
        datess = datetime.datetime.strptime(fechaInicios, '%Y-%m-%d').date()
        fechaFins = datess + datetime.timedelta(days=30)
        #octubre
        fechaInicioo = str(ano+'-10-1')
        dateso = datetime.datetime.strptime(fechaInicioo, '%Y-%m-%d').date()
        fechaFino = dateso + datetime.timedelta(days=30)
        #noviembre
        fechaInicion = str(ano+'-11-1')
        datesn = datetime.datetime.strptime(fechaInicion, '%Y-%m-%d').date()
        fechaFinn = datesn + datetime.timedelta(days=30)
        #diciembre
        fechaIniciod = str(ano+'-12-1')
        datesd = datetime.datetime.strptime(fechaIniciod, '%Y-%m-%d').date()
        fechaFind = datesd + datetime.timedelta(days=30)


        export = []
        export.append(['ACCIDENTES'])
        export.append(['Año', 'Mes', 'Fecha', 'Hora','Tipo Accidente', 'Ubicación', 'Cédula Agente Tránsito', 'Nombres Agente Tránsito'])
    #2019
        for inf in Accidente_Transito.objects.filter(Fecha__gte=datese1, Fecha__lte=fechaFine1):
            export.append([int(ano1), 'Enero', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesf1, Fecha__lte=fechaFinf1):
            export.append([int(ano1), 'Febrero', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesm1, Fecha__lte=fechaFinm1):
            export.append([int(ano1), 'Marzo', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesa1, Fecha__lte=fechaFina1):
            export.append([int(ano1), 'Abril', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesmy1, Fecha__lte=fechaFinmy1):
            export.append([int(ano1), 'Mayo', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesjn1, Fecha__lte=fechaFinjn1):
            export.append([int(ano1), 'Junio', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesjl1, Fecha__lte=fechaFinjl1):
            export.append([int(ano1), 'Julio', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesag1, Fecha__lte=fechaFinag1):
            export.append([int(ano1), 'Agosto', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datess1, Fecha__lte=fechaFins1):
            export.append([int(ano1), 'Septiembre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=dateso1, Fecha__lte=fechaFino1):
            export.append([int(ano1), 'Octubre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesn1, Fecha__lte=fechaFinn1):
            export.append([int(ano1), 'Noviembre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesd1, Fecha__lte=fechaFind1):
            export.append([int(ano1), 'Diciembre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])


    #2020
        for inf in Accidente_Transito.objects.filter(Fecha__gte=datese, Fecha__lte=fechaFine):
            export.append([int(ano), 'Enero', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesf, Fecha__lte=fechaFinf):
            export.append([int(ano), 'Febrero', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesm, Fecha__lte=fechaFinm):
            export.append([int(ano), 'Marzo', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesa, Fecha__lte=fechaFina):
            export.append([int(ano), 'Abril', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesmy, Fecha__lte=fechaFinmy):
            export.append([int(ano), 'Mayo', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesjn, Fecha__lte=fechaFinjn):
            export.append([int(ano), 'Junio', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesjl, Fecha__lte=fechaFinjl):
            export.append([int(ano), 'Julio', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesag, Fecha__lte=fechaFinag):
            export.append([int(ano), 'Agosto', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datess, Fecha__lte=fechaFins):
            export.append([int(ano), 'Septiembre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=dateso, Fecha__lte=fechaFino):
            export.append([int(ano), 'Octubre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesn, Fecha__lte=fechaFinn):
            export.append([int(ano), 'Noviembre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

        for inf in Accidente_Transito.objects.filter(Fecha__gte=datesd, Fecha__lte=fechaFind):
            export.append([int(ano), 'Diciembre', inf.Fecha, inf.Hora_Accidente, inf.TipoAccidente, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])
        
        sheet = excel.pe.Sheet(export)
        return excel.make_response(sheet, "xlsx", file_name="accidentes.xlsx")

