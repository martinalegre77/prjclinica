from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'), # ingreso a la app
    path('not-found/<str:user>', views.not_found, name='not-found'), # usuario no encontrado
    path('registro/<int:id>', views.registro, name='registro'), # registro de nuevo usuario
    path('menu/', views.menu, name='menu'), # menu de la app
    path('ingresar-datos/', views.ingresar_datos, name='ingresar-datos'),
    path('realizar-apto/', views.realizar_apto, name='realizar-apto'),
    path('re-login/', views.re_login, name='re-login'), # redireccionamiento a login
    path('list-instituciones/', views.listar_instituciones, name='listar-instituciones'), # listar instituciones
    path('add-institucion/', views.agregar_institucion, name='agregar-institucion'), # agregrar institución
    path('edit-institucion/<int:id>/', views.editar_institucion, name='editar-institucion'), # editar info institución
    path('list-deportes/', views.listar_deportes, name='listar-deportes'), # lista de deportes
    path('add-deporte/', views.agregar_deporte, name='agregar-deporte'), # agregar deporte
    path('edit-deporte/<int:id>/', views.editar_deporte, name='editar-deporte'), # editar info deporte
]