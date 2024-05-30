# from django import forms
from django.forms import ModelForm
from .models import AntFamiliares, AntPersonales, Apto, Deporte, Deportista, ExamenFisico, Institucion, Usuario


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


class AntFamiliaresForm(ModelForm):
    class Meta:
        model = AntFamiliares
        fields = '__all__'


class AntPersonalesForm(ModelForm):
    class Meta:
        model = AntPersonales
        fields = '__all__'


class ExamenFisicoForm(ModelForm):
    class Meta:
        model = ExamenFisico
        fields = '__all__'


class AptoForm(ModelForm):
    class Meta:
        model = Apto
        fields = '__all__'
