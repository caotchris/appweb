from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import exportar_csv, exportar_csv_intentos, ploteri2020, crearArticulos_COIP, crearInfraccion_Transito, listarInfraccion, ArticulosList, InfraccionList, buscar_intentos, buscar_infracciones, listarIntento, mapaIntento, mapaIntentoaccion, mapaInfraccion, buscar_infracciones_juez, Intento_Transito, Reportesadicionar, GeneratePdf, pinindex


urlpatterns = [
    path('crear_articulos_coip/', login_required(crearArticulos_COIP), name='crear_articulos_coip'),
    path('crear_infraccion_transito/', login_required(crearInfraccion_Transito), name='crear_infraccion_transito'),
    path('listar_infraccion_transito/', login_required(listarInfraccion), name='listar_infraccion_transito'),
    path('articulos/', ArticulosList.as_view(), name='articulos_list'),
    path('infraccion/', InfraccionList.as_view(), name='infraccion_list'),
    path('buscar_Intentos/', login_required(buscar_intentos), name='buscar_Intentos'),
    path('consultar_Infraccion/', login_required(buscar_infracciones), name='consultar_Infraccion'),
    path('consultar_Infraccion_juez/', login_required(buscar_infracciones_juez), name='consultar_Infraccion_juez'),
    path('listarIntento/', login_required(listarIntento)),
    path('mapaIntento/', login_required(mapaIntento)),
    path('mapaIntentoaccion/', login_required(mapaIntentoaccion)),
    path('mapaInfraccion/', login_required(mapaInfraccion)),
    path('Intento_Transito/', login_required(Intento_Transito)),
    path('Reportesadicionar/', login_required(Reportesadicionar)),
    path('pinindex/', login_required(pinindex)),
    path('GeneratePdf/', login_required(GeneratePdf.as_view())),

    path('ploteri2020/', login_required(ploteri2020)), #Insercion del grafico en html

    path('exportar_csv/', login_required(exportar_csv)), #Gener EXCEL

    path('exportar_csv_intentos/', login_required(exportar_csv_intentos)), #Gener EXCEL

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
