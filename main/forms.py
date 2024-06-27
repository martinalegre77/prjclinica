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


class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = '__all__'