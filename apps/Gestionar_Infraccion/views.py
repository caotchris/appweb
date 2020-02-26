from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import Articulos_COIPForm, Infraccion_TransitoForm, IntentosForm, ContadorInfForm
from apps.Gestionar_Informacion.forms import ConductorForm, VehiculoForm
from apps.Gestionar_Evidencia.forms import imageform, videoform, audioform
from .models import Infraccion_Transito, Articulos_COIP, Intentos, ContadorInfraccion
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ArticulosSerializer, InfraccionSerializer
from apps.Gestionar_Informacion.models import Conductor, Vehiculo
from apps.Gestionar_Evidencia.models import MyImage, MyVideo, MyAudio
from apps.Gestionar_Usuarios.models import Agente_Transito
from apps.Gestionar_Accidente.models import Accidente_Transito
from apps.Gestionar_Usuarios.forms import Agente_Transito_Form

from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
import datetime



from django.http import HttpResponse
from .utils import render_to_pdf #created in step 4
from django.template.loader import get_template

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        id = request.GET['Infraccion_Transito']
        infraccion = Infraccion_Transito.objects.all().filter(NumeroInfraccion=id)
        foto = MyImage.objects.all().filter(id_Evidencia=id)
        data = {'hour': datetime.datetime.now(), 'infraccion' : infraccion, 'foto': foto}
        pdf = render_to_pdf('Gestionar_Infraccion/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class ArticulosList(generics.ListCreateAPIView):
    queryset = Articulos_COIP.objects.all()
    serializer_class = ArticulosSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)


class InfraccionList(generics.ListCreateAPIView):
    queryset = Infraccion_Transito.objects.all()
    serializer_class = InfraccionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)


def home(request):
    infracciones = Infraccion_Transito.objects.all()
    accidentes = Accidente_Transito.objects.all()

    fechaInicio = request.POST.get('FechaInicio')
    fechaFin = request.POST.get('FechaFin')
    Tipo = request.POST.get('Tipo')


    if request.method == 'POST':
        if (str(fechaFin)+'' != '') & (str(fechaInicio)+'' != ''):
            try:

                if str(Tipo)+'' == 'Infracciones':
                    infracciones = Infraccion_Transito.objects.all().filter(Fecha_Infraccion__gte=fechaInicio, Fecha_Infraccion__lte=fechaFin)
                    return render(request, 'index.html', {'infracciones': infracciones})

                elif str(Tipo)+'' == 'Accidentes':
                    accidentes = Accidente_Transito.objects.filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin)
                    return render(request, 'index.html', {'accidentes': accidentes})
                else:
                    accidentes = Accidente_Transito.objects.filter(Fecha__gte=fechaInicio, Fecha__lte=fechaFin)
                    infracciones = Infraccion_Transito.objects.all().filter(Fecha_Infraccion__gte=fechaInicio, Fecha_Infraccion__lte=fechaFin)
                    return render(request, 'index.html', {'infracciones': infracciones, 'accidentes': accidentes})


            except Accidente_Transito.DoesNotExist:
                return render(request, 'index.html', {'infracciones': infracciones, 'accidentes': accidentes})

        else:
            return render(request, 'index.html', {'infracciones': infracciones, 'accidentes': accidentes})

    else:

        for inf in Infraccion_Transito.objects.all().filter(Estado='Reportado'):
            ac = datetime.date.today()
            s = str(inf.Fecha_Registro)

            dates = datetime.datetime.strptime(s, '%Y-%m-%d').date()
            modified_date = dates + datetime.timedelta(days=3)

            if ac >= modified_date:
                inf.Estado = 'Pendiente de pago'
                inf.save()
        return render(request, 'index.html', {'infracciones': infracciones, 'accidentes': accidentes})


def homejuez(request):
    return render(request, 'indexjuez.html')


def redireccionar(request):
    return render(request, 'redireccionar.html')



def crearArticulos_COIP(request):
    if request.method == 'POST':
        print(request.POST)
        articulos_coip_form = Articulos_COIPForm(request.POST)
        if articulos_coip_form.is_valid():
            articulos_coip_form.save()
            messages.warning(request, 'Registro Correcto')
            return redirect('index')
        else:
            messages.warning(request, 'Error en el formulario')
            return render(request, 'Gestionar_Infraccion/crear_articulos_coip.html', {'articulos_coip_form': articulos_coip_form})
    else:
        articulos_coip_form = Articulos_COIPForm()
        return render(request, 'Gestionar_Infraccion/crear_articulos_coip.html', {'articulos_coip_form': articulos_coip_form})


def crearInfraccion_Transito(request):
    if request.method == 'POST':
        infraccion_transito_form = Infraccion_TransitoForm(request.POST)
        articulos_coip_form = Articulos_COIPForm(request.POST)
        conductorform = ConductorForm(request.POST)
        vehiculoform = VehiculoForm(request.POST)
        audform = audioform(request.POST, request.FILES)
        vidform = videoform(request.POST, request.FILES)
        fotoform = imageform(request.POST, request.FILES)
        agenteform = Agente_Transito_Form(request.POST)
        contadorform =ContadorInfForm(request.POST)


        if infraccion_transito_form.is_valid() & articulos_coip_form.is_valid():

            agente = Agente_Transito.objects.get(Cedula=request.POST.get('Cedula'))

            contador = ContadorInfraccion()
            contador.CedulaAgente = request.POST.get('Cedula')
            contador.CodigoAgente = agente.Codigo_Agente
            contador.ContadorAgente = request.POST.get('ContadorInf')
            contador.save()

            agt =Agente_Transito()
            agt.Cedula = request.POST.get('Cedula')
            agt.Nombres = request.POST.get('Nombres')
            agt.Apellidos = request.POST.get('Apellidos')

            articulo = Articulos_COIP()
            articulo.Id_Articulo = request.POST.get('NumeroInfraccion')
            articulo.Articulo = request.POST.get('Articulo')
            articulo.Inciso = request.POST.get('Inciso')
            articulo.Numeral = request.POST.get('Numeral')
            articulo.save()

            cd = Conductor()
            cd.CedulaC = request.POST.get('CedulaC')
            cd.Nombres = request.POST.get('Nombres')
            cd.Apellidos = request.POST.get('Apellidos')
            cd.TipoLicencia = request.POST.get('TipoLicencia')
            cd.CategoriaLicencia = request.POST.get('CategoriaLicencia')
            cd.FechaEmisionLicencia= request.POST.get('FechaEmisionLicencia')
            cd.FechaCaducidadLicencia = request.POST.get('FechaCaducidadLicencia')

            vehiculo = Vehiculo()
            vehiculo.Placa = request.POST.get('Placa')
            vehiculo.Marca = request.POST.get('Marca')
            vehiculo.Tipo = request.POST.get('Tipo')
            vehiculo.Color = request.POST.get('Color')
            vehiculo.FechaMatricula = request.POST.get('FechaMatricula')
            vehiculo.FechaCaducidadMatricula = request.POST.get('FechaCaducidadMatricula')

            infraccionT = Infraccion_Transito()
            infraccionT.NumeroInfraccion = request.POST.get('NumeroInfraccion')
            infraccionT.Descripcion = request.POST.get('Descripcion')
            infraccionT.Ubicacion = request.POST.get('Ubicacion')
            infraccionT.Latitud = request.POST.get('Latitud')
            infraccionT.Longitud = request.POST.get('Longitud')
            infraccionT.Estado = request.POST.get('Estado')
            infraccionT.Fecha_Infraccion = request.POST.get('Fecha_Infraccion')
            infraccionT.Hora_Infraccion = request.POST.get('Hora_Infraccion')
            infraccionT.Hora_Detencion = request.POST.get('Hora_Detencion')
            infraccionT.Agente = agt
            infraccionT.ArticuloC = articulo
            infraccionT.Conductor = cd
            infraccionT.Vehiculo = vehiculo
            infraccionT.save()

            foto = MyImage()
            foto.model_pic = request.POST.get('model_pic')
            foto.id_Evidencia = request.POST.get('NumeroInfraccion')
            if foto.model_pic != '':
                foto.model_pic = request.FILES.get('model_pic')
                foto.save()

            audio = MyAudio()
            audio.model_aud = request.POST.get('model_aud')
            audio.id_Evidencia = request.POST.get('NumeroInfraccion')
            if audio.model_aud != '':
                audio.model_aud = request.FILES.get('model_aud')
                audio.save()

            video = MyVideo()
            video.model_vid = request.POST.get('model_vid')
            video.id_Evidencia = request.POST.get('NumeroInfraccion')
            if video.model_vid != '':
                video.model_vid = request.FILES.get('model_vid')
                video.save()

            messages.warning(request, 'Registro Correcto')
            return redirect('index')  # retorno de confirmacion
        else:
            messages.warning(request, 'Error en el formulario')
            return render(request,'Gestionar_Infraccion/crear_infraccion_transito.html',{'infraccion_transito_form':infraccion_transito_form, 'articulos_coip_form':articulos_coip_form, 'conductorform':conductorform, 'vehiculoform':vehiculoform, 'audform': audform, 'vidform': vidform, 'fotoform': fotoform, 'contadorform':contadorform, 'agenteform': agenteform})
    else:
        infraccion_transito_form = Infraccion_TransitoForm()
        articulos_coip_form = Articulos_COIPForm()
        conductorform = ConductorForm()
        vehiculoform = VehiculoForm()
        agenteform = Agente_Transito_Form()
        audform = audioform(request.POST, request.FILES)
        vidform = videoform(request.POST, request.FILES)
        fotoform = imageform(request.POST, request.FILES)
        contadorform =ContadorInfForm()
        messages.warning(request, 'Error')
        return render(request, 'Gestionar_Infraccion/crear_infraccion_transito.html', {'infraccion_transito_form': infraccion_transito_form, 'articulos_coip_form': articulos_coip_form, 'conductorform': conductorform, 'vehiculoform': vehiculoform, 'agenteform': agenteform, 'audform': audform, 'vidform': vidform, 'fotoform': fotoform})


def buscar_InfraccionNumAgente(request):
    if request.method == 'POST':
        codAgente = request.POST.get('Codigo_Agente')
        try:
            agente = Agente_Transito.objects.get(Codigo_Agente=codAgente)
        except Exception as e:
            raise e


def listarInfraccion(request):
    infracciones = Infraccion_Transito.objects.all()
    NumeroInfraccion = 0  # filtro por defecto
    if request.POST.get('NumeroInfraccion'):
        NumeroInfraccion = int(request.POST.get('NumeroInfraccion'))
        infracciones = infracciones.filter(
            NumeroInfraccion__gte=NumeroInfraccion)
    return render(request, 'Gestionar_Infraccion/listar_infraccion_transito.html', {'infracciones': infracciones, 'NumeroInfraccion': NumeroInfraccion})


def buscar_intentos(request):
    fechaInicio = request.POST.get('FechaInicio')
    fechaFin = request.POST.get('FechaFin')
    intentos = Intentos.objects.filter(Accion=0)
    Cedula = ''  # filtro por defecto
    intentoform = IntentosForm()
    intentoform = IntentosForm(request.POST)
    if request.POST.get('Cedula'):
        Cedula = int(request.POST.get('Cedula'))
        intentos = intentos.filter(Cedula=Cedula)

    if request.method == 'POST':
       if (str(fechaInicio)+'' != '') & (str(fechaFin)+'' != ''):
              intentos = intentos.filter(Fecha_Intento__gte=str(fechaInicio), Fecha_Intento__lte=str(fechaFin))

    return render(request, 'Gestionar_Infraccion/consultaIntentos.html', {'intentos': intentos, 'Cedula': Cedula, 'intentoform': intentoform})



def buscar_infracciones(request):
    if request.method == 'POST':
        numeroInfraccion = request.POST.get('NumeroInfraccion')
        fechaInicio = request.POST.get('FechaInicio')
        fechaFin = request.POST.get('FechaFin')
        conductor = request.POST.get('Conductor')
        vehiculo = request.POST.get('Vehiculo')
        estado = request.POST.get('Estado')
        Tipo = request.POST.get('Tipo')

        if (str(numeroInfraccion) != ''):
            try:
                infraccion = Infraccion_Transito.objects.all().filter(NumeroInfraccion=numeroInfraccion)
                contador = Infraccion_Transito.objects.all().filter(NumeroInfraccion=numeroInfraccion).count()
                context = {
                    'infraccion': infraccion,
                    'contador' : contador,
                }
                

                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html')
        elif (str(fechaInicio) != '') & (str(fechaFin) != ''):
            try:

                if str(Tipo)+'' == 'Todos':
                    infraccion = Infraccion_Transito.objects.all().filter(Fecha_Infraccion__gte=fechaInicio, Fecha_Infraccion__lte=fechaFin)
                    contador = Infraccion_Transito.objects.all().filter(Fecha_Infraccion__gte=fechaInicio, Fecha_Infraccion__lte=fechaFin).count()
                    context = {
                        'infraccion': infraccion,
                        'contador' : contador,
                    }
                else:
                    infraccion = Infraccion_Transito.objects.all().filter(Fecha_Infraccion__gte=fechaInicio, Fecha_Infraccion__lte=fechaFin, ArticuloC__Articulo__icontains=Tipo)
                    contador = Infraccion_Transito.objects.all().filter(Fecha_Infraccion__gte=fechaInicio, Fecha_Infraccion__lte=fechaFin, ArticuloC__Articulo__icontains=Tipo).count()
                    context = {
                        'infraccion': infraccion,
                        'contador' : contador,
                    }

                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html')

        elif (str(conductor) != ''):
            try:
                infraccion = Infraccion_Transito.objects.all().filter(Conductor=conductor)
                contador = Infraccion_Transito.objects.all().filter(Conductor=conductor).count()
                context = {
                    'infraccion': infraccion,
                    'contador' : contador,
                }
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html')

        elif (str(vehiculo) != ''):
            try:
                infraccion = Infraccion_Transito.objects.all().filter(Vehiculo=vehiculo)
                contador = Infraccion_Transito.objects.all().filter(Vehiculo=vehiculo).count()
                context = {
                    'infraccion': infraccion,
                    'contador' : contador,
                }
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html')

        elif (str(estado) != ''):
            try:
                infraccion = Infraccion_Transito.objects.all().filter(Estado=estado)
                contador = Infraccion_Transito.objects.all().filter(Estado=estado).count()
                context = {
                    'infraccion': infraccion,
                    'contador' : contador,
                }
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccion.html')

        else:
            messages.warning(request, "Ingrese numero")
            return render(request, 'Gestionar_Infraccion/consultaInfraccion.html')
    else:
        return render(request, 'Gestionar_Infraccion/consultaInfraccion.html')


def buscar_infracciones_juez(request):
    if request.method == 'POST':
        numeroInfraccion = request.POST.get('NumeroInfraccion')
        conductor = request.POST.get('Conductor')
        vehiculo = request.POST.get('Vehiculo')

        if (str(numeroInfraccion) != ''):
            try:
                infraccion = Infraccion_Transito.objects.all().filter(NumeroInfraccion=numeroInfraccion)
                contador = Infraccion_Transito.objects.all().filter(NumeroInfraccion=numeroInfraccion).count()
                context = {
                    'infraccion': infraccion,
                    'contador' : contador,
                }
                return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html')
        elif (str(conductor) != ''):
            try:
                infraccion = Infraccion_Transito.objects.all().filter(Conductor=conductor)
                contador = Infraccion_Transito.objects.all().filter(Conductor=conductor).count()
                context = {
                    'infraccion': infraccion,
                    'contador' : contador,
                }
                return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html')

        elif (str(vehiculo) != ''):
            try:
                infraccion = Infraccion_Transito.objects.all().filter(Vehiculo=vehiculo)
                contador = Infraccion_Transito.objects.all().filter(Vehiculo=vehiculo).count()
                context = {
                    'infraccion': infraccion,
                    'contador' : contador,
                }
                return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html', context)
            except Exception as e:
                messages.warning(request, "No encontrado")
                return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html')

        else:
            messages.warning(request, "Ingrese numero")
            return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html')
    else:
        return render(request, 'Gestionar_Infraccion/consultaInfraccionjuez.html')


def listarIntento(request):
    id = request.GET['Intentos']
    intentos = Intentos.objects.all().filter(Cedula=id, Accion=1)
    fechaInicio = request.POST.get('FechaInicio')
    fechaFin = request.POST.get('FechaFin')

    context = {'intentos': intentos,}
    return render(request, 'Gestionar_Infraccion/intentoControl.html', context)


def mapaIntento(request):
    if request.method == 'POST':
        id = request.GET['Intentos']
        intentos1 = Intentos.objects.get(id=id)
        intentos1.Descripcion = request.POST.get('Descripcion')
        intentos1.Accion=1
        intentos1.save()
        messages.warning(request, 'Actualizacion correcta')
        return redirect('/Gestionar_Infraccion/buscar_Intentos/')
    else:
        intentoform = IntentosForm()
        id = request.GET['Intentos']
        intentos = Intentos.objects.all().filter(id=id)

        context = {'intentos': intentos,'intentoform': intentoform,}

        return render(request, 'Gestionar_Infraccion/mapaintento.html', context)

def mapaIntentoaccion(request):
    intentoform = IntentosForm()
    id = request.GET['Intentos']
    intentos = Intentos.objects.all().filter(id=id)
    context = {'intentos': intentos,'intentoform': intentoform,}
    return render(request, 'Gestionar_Infraccion/mapaintentoaccion.html', context)


def mapaInfraccion(request):
    if request.method == 'GET':
        id = request.GET['Infraccion_Transito']
        infraccion = Infraccion_Transito.objects.all().filter(NumeroInfraccion=id)

    context = {'infraccion': infraccion,
               }
    return render(request, 'Gestionar_Infraccion/mapaInfraccion.html', context)


def Reportesadicionar(request):
    if request.method == 'POST':
        audform = audioform(request.POST, request.FILES)
        vidform = videoform(request.POST, request.FILES)
        fotoform = imageform(request.POST, request.FILES)
        id = request.GET['Infraccion_Transito']
        infraccion1 = Infraccion_Transito.objects.get(NumeroInfraccion=id)



        if infraccion1.Estado == 'Impugnada':
            infraccion_form = Infraccion_TransitoForm()
            audform = audioform(request.POST, request.FILES)
            vidform = videoform(request.POST, request.FILES)
            fotoform = imageform(request.POST, request.FILES)
            id = request.GET['Infraccion_Transito']
            infraccion = Infraccion_Transito.objects.all().filter(NumeroInfraccion=id)
            context = {'infraccion': infraccion, 'infraccion_form': infraccion_form, 'audform': audform, 'vidform': vidform, 'fotoform': fotoform}
            messages.warning(request, 'No se puede modificar este estado')
            return render(request, 'Gestionar_Infraccion/reportes.html', context)

        if infraccion1.Estado == 'No impugnada':
            messages.warning(request, 'No se puede modificar este estado')
            return render(request, 'Gestionar_Infraccion/reportes.html')

        if infraccion1.Estado == 'Pendiente de pago':
            messages.warning(request, 'No se puede modificar este estado')
            return render(request, 'Gestionar_Infraccion/reportes.html')

        if infraccion1.Estado == 'Pagada':
            messages.warning(request, 'No se puede modificar este estado')
            return render(request, 'Gestionar_Infraccion/reportes.html')


        infraccion1.Estado = request.POST.get('Estado')


        if infraccion1.Estado == 'No impugnada':
            infraccion1.Estado = 'Pendiente de pago'
        infraccion1.save()


        foto = MyImage()
        foto.model_pic = request.POST.get('model_pic')
        foto.id_Evidencia = request.GET['Infraccion_Transito']
        if foto.model_pic != '':
            foto.model_pic = request.FILES.get('model_pic')
            foto.save()

        audio = MyAudio()
        audio.model_aud = request.POST.get('model_aud')
        audio.id_Evidencia = request.GET['Infraccion_Transito']
        if audio.model_aud != '':
            audio.model_aud = request.FILES.get('model_aud')
            audio.save()

        video = MyVideo()
        video.model_vid = request.POST.get('model_vid')
        video.id_Evidencia = request.GET['Infraccion_Transito']
        if video.model_vid != '':
            video.model_vid = request.FILES.get('model_vid')
            video.save()

        messages.warning(request, 'Actualizacion correcta')
        return redirect('/Gestionar_Infraccion/consultar_Infraccion/')
    else:
        infraccion_form = Infraccion_TransitoForm()
        audform = audioform(request.POST, request.FILES)
        vidform = videoform(request.POST, request.FILES)
        fotoform = imageform(request.POST, request.FILES)
        id = request.GET['Infraccion_Transito']
        infraccion = Infraccion_Transito.objects.all().filter(NumeroInfraccion=id)
        context = {'infraccion': infraccion, 'infraccion_form': infraccion_form, 'audform': audform, 'vidform': vidform, 'fotoform': fotoform}
        return render(request, 'Gestionar_Infraccion/reportes.html', context)


def Intento_Transito(request):
    if request.method == 'POST':
        id = request.GET('Intentos')
        try:
            intento = Intentos.objects.all.filter(id=id)
            intento.Descripcion = request.POST.get('Descripcion')
            intento.Accion = 1
            intento.save()
            messages.warning(request, 'Actualizacion correcta')
            return redirect('/Gestionar_Infraccion/buscar_Intentos/')

        except Exception as e:
            accidente_transitoForm = Accidente_TransitoForm()
            messages.warning(request, 'Numero Incorrecto')
            return redirect('/Gestionar_Infraccion/buscar_Intentos/')

def pinindex(request):
    try:
        id = request.GET['Infraccion_Transito']
        infraccion = Infraccion_Transito.objects.all().filter(NumeroInfraccion=id)
        context = {'infraccion': infraccion}
        messages.warning(request, 'Actualizacion correcta')
        return render(request, 'Gestionar_Infraccion/infraccionpin.html', context)

    except Exception as e:
        messages.warning(request, 'Actualizacion correcta')
        return redirect('/index/')





# Estadistica basica

import io
import matplotlib.pyplot as plt

from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg


def ploteri2020(request):
    if request.method == 'POST':
        TipoInfraccion = request.POST.get('TipoInfraccion')
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

        if str(TipoInfraccion)+'' == 'Todos':

            enero = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datese, Fecha_Infraccion__lte=fechaFine).count()
            febrero = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesf, Fecha_Infraccion__lte=fechaFinf).count()
            marzo = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesm, Fecha_Infraccion__lte=fechaFinm).count()
            abril = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesa, Fecha_Infraccion__lte=fechaFina).count()
            mayo = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesmy, Fecha_Infraccion__lte=fechaFinmy).count()
            junio = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjn, Fecha_Infraccion__lte=fechaFinjn).count()
            julio = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjl, Fecha_Infraccion__lte=fechaFinjl).count()
            agosto = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesag, Fecha_Infraccion__lte=fechaFinag).count()
            septiembre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datess, Fecha_Infraccion__lte=fechaFins).count()
            octubre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=dateso, Fecha_Infraccion__lte=fechaFino).count()
            noviembre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesn, Fecha_Infraccion__lte=fechaFinn).count()
            diciembre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesd, Fecha_Infraccion__lte=fechaFind).count()

        else:
            enero = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datese, Fecha_Infraccion__lte=fechaFine, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            febrero = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesf, Fecha_Infraccion__lte=fechaFinf, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            marzo = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesm, Fecha_Infraccion__lte=fechaFinm, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            abril = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesa, Fecha_Infraccion__lte=fechaFina, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            mayo = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesmy, Fecha_Infraccion__lte=fechaFinmy, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            junio = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjn, Fecha_Infraccion__lte=fechaFinjn, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            julio = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjl, Fecha_Infraccion__lte=fechaFinjl, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            agosto = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesag, Fecha_Infraccion__lte=fechaFinag, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            septiembre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datess, Fecha_Infraccion__lte=fechaFins, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            octubre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=dateso, Fecha_Infraccion__lte=fechaFino, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            noviembre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesn, Fecha_Infraccion__lte=fechaFinn, ArticuloC__Articulo__icontains=TipoInfraccion).count()
            diciembre = Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesd, Fecha_Infraccion__lte=fechaFind, ArticuloC__Articulo__icontains=TipoInfraccion).count()


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
        axes.set_ylabel("Infracciones")
        axes.set_title("GRAFICO INFRACCIONES"+" "+ano+" "+TipoInfraccion)
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

        return render(request, "Gestionar_Infraccion/estadistica2020.html", context)

    else:
        return render(request, "Gestionar_Infraccion/estadistica2020.html")



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
    export.append(['INFRACCIONES'])
    export.append(['Año', 'Mes', 'Fecha', 'Hora','Artículo', "Inciso/Descripción", "Numeral", 'Cédula Conductor', 'Nombres Conductor', 'Puntos Conductor', 'Placa Vehículo', 'Ubicación', 'Cédula Agente Tránsito', 'Nombres Agente Tránsito'])


#2019
    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datese1, Fecha_Infraccion__lte=fechaFine1):
        export.append([int(ano1), 'Enero', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesf1, Fecha_Infraccion__lte=fechaFinf1):
        export.append([int(ano1), 'Febrero', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesm1, Fecha_Infraccion__lte=fechaFinm1):
        export.append([int(ano1), 'Marzo', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesa1, Fecha_Infraccion__lte=fechaFina1):
        export.append([int(ano1), 'Abril', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesmy1, Fecha_Infraccion__lte=fechaFinmy1):
        export.append([int(ano1), 'Mayo', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjn1, Fecha_Infraccion__lte=fechaFinjn1):
        export.append([int(ano1), 'Junio', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjl1, Fecha_Infraccion__lte=fechaFinjl1):
        export.append([int(ano1), 'Julio', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesag1, Fecha_Infraccion__lte=fechaFinag1):
        export.append([int(ano1), 'Agosto', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datess1, Fecha_Infraccion__lte=fechaFins1):
        export.append([int(ano1), 'Septiembre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=dateso1, Fecha_Infraccion__lte=fechaFino1):
        export.append([int(ano1), 'Octubre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesn1, Fecha_Infraccion__lte=fechaFinn1):
        export.append([int(ano1), 'Noviembre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesd1, Fecha_Infraccion__lte=fechaFind1):
        export.append([int(ano1), 'Diciembre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

#2020
    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datese, Fecha_Infraccion__lte=fechaFine):
        export.append([int(ano), 'Enero', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesf, Fecha_Infraccion__lte=fechaFinf):
        export.append([int(ano), 'Febrero', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesm, Fecha_Infraccion__lte=fechaFinm):
        export.append([int(ano), 'Marzo', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesa, Fecha_Infraccion__lte=fechaFina):
        export.append([int(ano), 'Abril', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesmy, Fecha_Infraccion__lte=fechaFinmy):
        export.append([int(ano), 'Mayo', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjn, Fecha_Infraccion__lte=fechaFinjn):
        export.append([int(ano), 'Junio', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesjl, Fecha_Infraccion__lte=fechaFinjl):
        export.append([int(ano), 'Julio', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesag, Fecha_Infraccion__lte=fechaFinag):
        export.append([int(ano), 'Agosto', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datess, Fecha_Infraccion__lte=fechaFins):
        export.append([int(ano), 'Septiembre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=dateso, Fecha_Infraccion__lte=fechaFino):
        export.append([int(ano), 'Octubre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesn, Fecha_Infraccion__lte=fechaFinn):
        export.append([int(ano), 'Noviembre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    for inf in Infraccion_Transito.objects.filter(Fecha_Infraccion__gte=datesd, Fecha_Infraccion__lte=fechaFind):
        export.append([int(ano), 'Diciembre', inf.Fecha_Infraccion, inf.Hora_Infraccion, inf.ArticuloC.Articulo, inf.ArticuloC.Inciso, inf.ArticuloC.Numeral, int(inf.Conductor.CedulaC), inf.Conductor.Nombres+' '+inf.Conductor.Apellidos, int(inf.Conductor.Puntos), inf.Vehiculo.Placa, inf.Ubicacion, inf.Agente.Cedula, inf.Agente.Nombres+' '+inf.Agente.Apellidos])

    sheet = excel.pe.Sheet(export)
    return excel.make_response(sheet, "xlsx", file_name="infracciones.xlsx")




def exportar_csv_intentos(request):
    ano = '2020'
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
    export.append(['INTENTOS AGENTES TRÁNSITO'])
    export.append(['Año', 'Mes', 'Fecha', 'Hora','Cédula', "Nombres", "Acción=1:Atendido/0:Pendiente", 'Descripción', 'Ubicación'])

#2020
    for inf in Intentos.objects.filter(Fecha_Intento__gte=datese, Fecha_Intento__lte=fechaFine):
        export.append([int(ano), 'Enero', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesf, Fecha_Intento__lte=fechaFinf):
        export.append([int(ano), 'Febrero', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesm, Fecha_Intento__lte=fechaFinm):
        export.append([int(ano), 'Marzo', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesa, Fecha_Intento__lte=fechaFina):
        export.append([int(ano), 'Abril', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesmy, Fecha_Intento__lte=fechaFinmy):
        export.append([int(ano), 'Mayo', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesjn, Fecha_Intento__lte=fechaFinjn):
        export.append([int(ano), 'Junio', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesjl, Fecha_Intento__lte=fechaFinjl):
        export.append([int(ano), 'Julio', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesag, Fecha_Intento__lte=fechaFinag):
        export.append([int(ano), 'Agosto', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datess, Fecha_Intento__lte=fechaFins):
        export.append([int(ano), 'Septiembre', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=dateso, Fecha_Intento__lte=fechaFino):
        export.append([int(ano), 'Octubre', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesn, Fecha_Intento__lte=fechaFinn):
        export.append([int(ano), 'Noviembre', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    for inf in Intentos.objects.filter(Fecha_Intento__gte=datesd, Fecha_Intento__lte=fechaFind):
        export.append([int(ano), 'Diciembre', inf.Fecha_Intento, inf.Hora_Intento, int(inf.Agente.Cedula), inf.Agente.Nombres+' '+inf.Agente.Apellidos, int(inf.Accion), inf.Descripcion, inf.Ubicacion])

    sheet = excel.pe.Sheet(export)
    return excel.make_response(sheet, "xlsx", file_name="intentos.xlsx")