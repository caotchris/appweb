from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Agente_Transito
from django.contrib.admin import widgets
from django.urls import reverse_lazy


class Agente_Transito_Form(forms.ModelForm):
    class Meta:
        model = Agente_Transito
        fields = ['Codigo_Agente', 'Cedula', 'Nombres', 'Apellidos', 'fotoA']
        labels = {
            'Codigo_Agente': 'Código',
            'Cedula': 'Cédula',
            'Nombres': 'Nombres',
            'Apellidos': 'Apellidos'
        }
        widgets = {
            'Cedula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'cedula',
                    'readonly': 'readonly'
                }
            ),
            'Nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'nombres',
                    'readonly': 'readonly'
                }
            ),
            'Apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'apellidos',
                    'readonly': 'readonly'
                }
            )
        }

class Agente_Transito_Form1(forms.ModelForm):
    class Meta:
        model = Agente_Transito
        fields = ['Codigo_Agente', 'Cedula', 'Nombres', 'Apellidos', 'Clave', 'fotoA']
        labels = {
            'Codigo_Agente': 'Código',
            'Cedula': 'Cédula',
            'Nombres': 'Nombres',
            'Apellidos': 'Apellidos'
        }
        widgets = {
            'Codigo_Agente': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'codigo',
                }
            ),

            'Cedula': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'cedula',
                }
            ),
            'Nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'nombres',
                }
            ),
            'Apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'apellidos',
                }
            )
        }


class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
                'username',
                'first_name',
                'last_name',
                'email',
        ]

        labels = {
                'username': 'Nombre de usuario',
                'first_name': 'Nombres',
                'last_name': 'Apellidos',
                'email':    'Correo',
        }