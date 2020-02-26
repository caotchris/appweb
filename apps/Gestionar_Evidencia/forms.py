from django import forms
from .models import MyImage, MyAudio, MyVideo
from django.contrib.admin import widgets

class imageform(forms.ModelForm):
    model_pic = forms.FileField(required=False)

    class Meta:
        model = MyImage
        fields = [
            'model_pic',
            'id_Evidencia',
        ]


class videoform(forms.ModelForm):
    model_vid = forms.FileField(required=False)

    class Meta:
        model = MyVideo
        fields = [
            'model_vid',
            'id_Evidencia',
        ]


class audioform(forms.ModelForm):
    model_aud = forms.FileField(required=False)

    class Meta:
        model = MyAudio
        fields = [
            'model_aud',
            'id_Evidencia',
        ]
