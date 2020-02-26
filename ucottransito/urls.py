"""ucottransito URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework.authtoken import views
from django.conf.urls.static import static
from apps.Gestionar_Infraccion.views import home, homejuez, redireccionar
from apps.Gestionar_Usuarios.views import homeadmin
from apps.Gestionar_Usuarios.views import Login, Logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', login_required(home), name='index'),
    path('homejuez/', login_required(homejuez), name='indexjuez'),
    path('homeadmin/', login_required(homeadmin), name='indexadmin'),
    path('', login_required(redireccionar), name='redireccionar'),
    path('Gestionar_Infraccion/', include(('apps.Gestionar_Infraccion.urls', 'Gestionar_Infraccion'))),
    path('Gestionar_Accidente/', include(('apps.Gestionar_Accidente.urls', 'Gestionar_Accidente'))),
    path('Gestionar_Usuarios/', include(('apps.Gestionar_Usuarios.urls', 'Gestionar_Usuarios'))),
    path('Gestionar_Informacion/', include(('apps.Gestionar_Informacion.urls', 'Gestionar_Informacion'))),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', Logout, name='logout'),
    path('api_generate_token/', views.obtain_auth_token),
    path('servicio_web/', include(('apps.servicio_web.urls', 'servicio_web'))),
    path('Gestionar_Evidencia/', include('apps.Gestionar_Evidencia.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
