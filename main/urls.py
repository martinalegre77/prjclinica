from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('not-found/<str:user>', views.not_found, name='not-found'),
    path('registro/<int:id>', views.registro, name='registro'),
    path('consultar/', views.consultar, name='consultar'),
    path('ingresar-datos/', views.ingresar_datos, name='ingresar-datos'),
    path('realizar-apto/', views.realizar_apto, name='realizar-apto'),
    path('re-login/', views.re_login, name='re-login'),
    path('list-instituciones/', views.listar_instituciones, name='listar-instituciones'),
    path('add-institucion/', views.agregar_institucion, name='agregar-institucion'),
    path('edit-institucion/<int:id>/', views.editar_institucion, name='editar-institucion'),
    path('list-deportes/', views.listar_deportes, name='listar-deportes'),
    path('add-deporte/', views.agregar_deporte, name='agregar-deporte'),
    path('edit-deporte/<int:id>/', views.editar_deporte, name='editar-deporte'),
]