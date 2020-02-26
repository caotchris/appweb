from rest_framework import serializers
from .models import MyImage, MyVideo, MyAudio

class imageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyImage
        fields = [
            'model_pic',
            'id_Evidencia',
        ]


class videoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyVideo
        fields = [
            'model_vid',
            'id_Evidencia',
        ]


class audioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAudio
        fields = [
            'model_aud',
            'id_Evidencia',
        ]
