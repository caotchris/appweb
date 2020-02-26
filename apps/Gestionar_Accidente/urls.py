from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .views import exportar_csv, ploter2020, crearAccidente_Transito, AccidenteList, buscarAccidente_Transito, detalleAccidente_Transito, mapaAccidente, crearAccidente_Transito_juez, Reportesadicionara, apinindex

urlpatterns = [
    path('crear_accidente_transito/', login_required(crearAccidente_Transito),
         name='crear_accidente_transito'),
    path('crear_accidente_transito_juez/', login_required(crearAccidente_Transito_juez),
         name='crear_accidente_transito_juez'),
    path('accidente/', login_required(AccidenteList.as_view()), name='accidente_list'),
    path('bucar_accidente_transito/', login_required(buscarAccidente_Transito),
         name='buscar_accidente_transito'),
    path('detalle_accidente_transito/', login_required(detalleAccidente_Transito),
         name='detalle_accidente_transito'),
    path('mapaAccidente/', login_required(mapaAccidente)),
    path('Reportesadicionara/', login_required(Reportesadicionara)),
    path('apinindex/', login_required(apinindex)),

    path('ploter2020/', login_required(ploter2020)), #Insercion del grafico en html


    path('exportar_csv/', login_required(exportar_csv)), #Gener EXCEL

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
