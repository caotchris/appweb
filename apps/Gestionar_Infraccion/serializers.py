from rest_framework import serializers
from .models import Articulos_COIP, Infraccion_Transito, Intentos, ContadorInfraccion, ArticulosBD, IncisosBD, NumeralBD


class ArticulosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulos_COIP
        fields = (
            'Id_Articulo',
            'Articulo',
            'Inciso',
            'Numeral',
        )


class InfraccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infraccion_Transito
        fields = (
            'NumeroInfraccion',
            'Descripcion',
            'Ubicacion',
            'Latitud',
            'Longitud',
            'Estado',
            'Fecha_Infraccion',
            'Hora_Infraccion',
            'Hora_Detencion',
            'Agente',
            'ArticuloC',
            'Conductor',
            'Vehiculo',
        )


class IntentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intentos
        fields = (
            'Cedula',
            'Latitud',
            'Longitud',
            'Ubicacion',
            'Fecha_Intento',
            'Hora_Intento',
            'Agente',
            'Descripcion',
            'Accion',
        )


class ContadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContadorInfraccion
        fields = (
            'CedulaAgente',
            'CodigoAgente',
            'ContadorAgente',
        )


class ArticulosBDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticulosBD
        fields = (
            'NumeroArticuloBD',
            'DescripcionBDA',
        )


class IncisosBDSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncisosBD
        fields = (
            'NumeroIncisoBD',
            'DescripcionBDI',
        )


class NumeralBDSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumeralBD
        fields = (
            'NumeroNumeralBD',
            'DescripcionBDN',
        )
