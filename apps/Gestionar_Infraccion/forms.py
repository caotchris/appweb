from django import forms
from .models import Infraccion_Transito, Articulos_COIP, Intentos, ContadorInfraccion
from django.contrib.admin import widgets
import datetime
import time


class Articulos_COIPForm(forms.ModelForm):
    class Meta:
        model = Articulos_COIP
        fields = ['Articulo', 'Inciso', 'Numeral']
        labels = {
            'Id_Articulo': 'Id Artículo',
            'Articulo': 'Artículo',
            'Inciso': 'Inciso',
            'Numeral': 'Numeral'
        }
        widgets = {
            'Articulo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del articulo',
                    'id': 'articulo',
                    'readonly': 'readonly'
                }
            ),
            'Inciso': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del inciso',
                    'id': 'inciso',
                    'readonly': 'readonly'
                }
            ),
            'Numeral': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del númeral',
                    'id': 'numeral',
                    'readonly': 'readonly'
                }
            ),
        }


class Infraccion_TransitoForm(forms.ModelForm):
    class Meta:
        model = Infraccion_Transito
        fields = ['NumeroInfraccion', 'Descripcion', 'Ubicacion',
                  'Fecha_Infraccion', 'Hora_Infraccion', 'Latitud', 'Longitud', 'Estado', 'Hora_Detencion']
        labels = {
            'NumeroInfraccion': 'Numero de Infracción',
            'Descripcion': 'Descripción',
            'Ubicacion': 'Ubicación',
            'Fecha_Infraccion': 'Fecha de la infracción',
            'Hora_Infraccion': 'Hora de la infracción',
            'Estado': 'Estado',
            'Hora_Detencion': 'Hora de la detención',
        }
        widgets = {
            'NumeroInfraccion': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese número infracción',
                    'readonly': 'readonly'
                }
            ),
            'Descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descripción',
                    'id': 'descripcion'
                }
            ),
            'Ubicacion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la ubicación',
                    'id': 'ubicacion'
                }
            ),
            'Fecha_Infraccion': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'Hora_Infraccion': forms.TimeInput(attrs={
                'class': 'form-control',
                'value': time.strftime("%H:%M:%S")
            }),
            'Hora_Detencion': forms.TimeInput(attrs={
                'class': 'form-control',
                'value': time.strftime("%H:%M:%S")
            }),
            'Estado': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
        }


class IntentosForm(forms.ModelForm):
    class Meta:
        model = Intentos
        fields = ['Cedula',
                  'Latitud',
                  'Longitud',
                  'Ubicacion',
                  'Fecha_Intento',
                  'Hora_Intento',
                  'Descripcion',
                  'Accion',
                  ]

        widgets = {
            'Descripcion': forms.Textarea(
                attrs={
                    'id': 'descripcion'
                }
            ),
        }

class ContadorInfForm(forms.ModelForm):
    class Meta:
        model = ContadorInfraccion
        fields = ['CedulaAgente',
                  'CodigoAgente',
                  'ContadorAgente',
                  ]
