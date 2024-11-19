from django import forms
from django.forms import ModelForm
from .models import Deporte, Deportista, Evaluacion, Institucion, Usuario


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        # db_table = ''
        # managed = True
        # verbose_name = 'ModelName'
        # verbose_name_plural = 'ModelNames'


class DeporteForm(ModelForm):
    class Meta:
        model = Deporte
        fields = '__all__'


class InstitucionForm(ModelForm):
    class Meta:
        model = Institucion
        fields = '__all__'


class DeportistaForm(ModelForm):
    class Meta:
        model = Deportista
        fields = '__all__'
        widgets = {
            'fecha_nac': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Mes/Dia/Año'
            }),
            'dni': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Solo números, sin puntos'
            }),
            'telefono': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Sin 0 y sin 15'
            }),
        }


class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = '__all__'
        widgets = {
            'talla': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. 1.65'
            }),
            'peso': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. 70.500'
            }),
            'oxigeno_sangre': forms.DateInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. 96'
            }),
        }


