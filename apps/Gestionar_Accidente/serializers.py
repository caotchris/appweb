from rest_framework import serializers
from .models import Accidente_Transito, ContadorAccidente


class AccidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accidente_Transito
        fields = (
            'NumeroAccidente',
            'TipoAccidente',
            'Descripcion',
            'Ubicacion',
            'Latitud',
            'Longitud',
            'Estado',
            'Fecha',
            'Hora_Registro',
            'Hora_Accidente',
            'Agente'
        )

class ContadorAccSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContadorAccidente
        fields = (
            'CedulaAgente',
            'CodigoAgente',
            'ContadorAgente',
        )
