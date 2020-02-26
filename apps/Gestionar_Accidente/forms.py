from django import forms
from .models import Accidente_Transito


class Accidente_TransitoForm(forms.ModelForm):
    class Meta:
        model = Accidente_Transito
        fields = ['NumeroAccidente',
                  'TipoAccidente',
                  'Descripcion',
                  'Ubicacion',
                  'Latitud',
                  'Longitud',
                  'Estado',
                  'Fecha',
                  'Hora_Registro',
                  'Hora_Accidente',

                  ]
        labels = {
            'NumeroAccidente': 'Número accidente',
            'TipoAccidente': 'Tipo accidente',
        }

        widgets = {
            'NumeroAccidente': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del articulo',

                }
            ),
            'TipoAccidente': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del inciso',
                    'readonly': 'readonly'

                }
            ),
            'Descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del númeral',
                    'readonly': 'readonly'

                }
            ),
            'Ubicacion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del númeral',
                    'readonly': 'readonly'
                }
            ),
            'Estado': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número del númeral',

                }
            ),
        }
