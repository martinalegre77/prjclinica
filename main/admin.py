from django.contrib import admin
from .models import AntFamiliares, AntPersonales, Apto, Deporte, Deportista, ExamenFisico, Institucion, Usuario

# Register your models here.

admin.site.register(Usuario) # Para que aparezca en el sitio Admin
admin.site.register(Deporte) 
admin.site.register(Institucion) 
admin.site.register(Deportista) 
admin.site.register(AntFamiliares) 
admin.site.register(AntPersonales) 
admin.site.register(ExamenFisico) 
admin.site.register(Apto) 

