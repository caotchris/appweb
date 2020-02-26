from django import forms
from .models import Conductor, Vehiculo
from django.contrib.admin import widgets


class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['CedulaC', 'Nombres', 'Apellidos', 'TipoLicencia',
                  'CategoriaLicencia', 'FechaEmisionLicencia', 'FechaCaducidadLicencia', 'Puntos']
        labels = {
            'CedulaC': 'Cédula',
            'Nombres': 'Nombres',
            'Apellidos': 'Apellidos',
            'TipoLicencia': 'Tipo de licencia',
            'CategoriaLicencia': 'Categoría de licencia',
            'FechaEmisionLicencia': 'Fecha de emisión licencia',
            'FechaCaducidadLicencia': 'Fecha caducidad licencia',
            'Puntos': 'Puntos'
        }
        widgets = {
            'CedulaC': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número de cédula',
                    'readonly': 'readonly'
                }
            ),
            'Nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los 2 nombres',
                    'readonly': 'readonly'
                }
            ),
            'Apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los 2 apellidos',
                    'readonly': 'readonly'
                }
            ),
            'TipoLicencia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el tipo de licencia',
                    'readonly': 'readonly'
                }
            ),
            'CategoriaLicencia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese categoría licencia',
                    'readonly': 'readonly'
                }
            ),
            'FechaEmisionLicencia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                }
            ),
            'FechaCaducidadLicencia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                }
            ),
            'Puntos': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly',
                }
            ),
        }


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['Placa', 'Marca', 'Tipo', 'Color',
                  'FechaMatricula', 'FechaCaducidadMatricula']
        labels = {
            'Placa': 'Placa',
            'Marca': 'Marca',
            'Tipo': 'Tipo',
            'Color': 'Color',
            'FechaMatricula': 'Fecha de matrícula',
            'FechaCaducidadMatricula': 'Fecha caducidad matrícula'
        }
        widgets = {
            'Placa': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese placa de vehículo',
                    'id': 'placa',
                    'readonly': 'readonly'
                }
            ),
            'Marca': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la marca',
                    'id': 'marca',
                    'readonly': 'readonly'
                }
            ),
            'Tipo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el tipo de vehículo',
                    'id': 'tipo',
                    'readonly': 'readonly'
                }
            ),
            'Color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese color de vehículo',
                    'readonly': 'readonly'
                }
            ),
            'FechaMatricula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                }
            ),
            'FechaCaducidadMatricula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                }
            ),
        }
