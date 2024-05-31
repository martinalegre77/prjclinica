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
    path('instituciones/', views.instituciones, name='instituciones'),
    path('deportes/', views.deportes, name='deportes'),
]