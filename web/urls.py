from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan-aptos/', views.scan_aptos, name='scan-aptos'),
    path('consulta-deportista/<int:qr>/', views.consulta_deportista, name='consulta-deportista'),
    path('no-encontrado/<int:qr>/', views.no_encontrado, name='no-encontrado'),
]