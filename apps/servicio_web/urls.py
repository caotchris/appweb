from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('crearinfraccion/', crearInfraccionServicio),
    path('detalleinfraccion/<int:pk>', detalleInfraccion),
    path('detalleinfraccionScript/<int:pk>', detalleInfraccionScript),

    path('crearAccidente/', crearAccidenteServicio),
    path('detalleAccidente/<int:pk>', detalleAccidente),
    path('detalleVehiculo/<str:pk>', detalleVehiculoServicio),

    path('detalleConductor/<int:pk>', detalleConductorSerializer),

    path('crearNumeroInfraccion/', crearNumeroInfraccionServicio),
    path('detalleNumeroInfraccion/<int:pk>', detalleNumeroInfraccionAgente),

    path('loginAgente', loginAgente),
    path('detalleAgente/<int:pk>', detalleAgente, name="detalleAgente"),

    path('crearIntento/', crearIntentoServicio),
    path('detalleIntento/<int:pk>', detalleIntento),

    path('crearArticulo/', crearArticuloServicio),

    path('detallecontador/<int:pk>', detallecontador), #contador de infracciones
    path('crearcontadorInf/', crearcontadorInf),

    path('detallecontadoracc/<int:pk>', detallecontadoracc), #contador de accidentes
    path('crearcontadorAcc/', crearcontadorAcc),

    path('detallearticulos/<int:pk>', detallearticulos),
    path('detalleincisos/<int:pk>', detalleincisos),
    path('detallenumeral/<int:pk>', detallenumeral),

    path('autenticacion', autenticacion),

]
