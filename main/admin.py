from django.contrib import admin
from .models import Deporte, Deportista, Institucion, Usuario, Evaluacion

# Register your models here.

admin.site.register(Usuario) # Para que aparezca en el sitio Admin
admin.site.register(Deporte) 
admin.site.register(Institucion) 
admin.site.register(Deportista) 
admin.site.register(Evaluacion)

