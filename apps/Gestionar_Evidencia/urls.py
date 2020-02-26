from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import serializers, viewsets, routers

urlpatterns = [
    path('listarEvidencia/', listarEvidencia),
    path('listarEvidenciaa/', listarEvidenciaa),
    path('upload/', ImageCreateAPIView.as_view()),
    path('uploadv/', VideoCreateAPIView.as_view()),
    path('uploada/', AudioCreateAPIView.as_view()),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
