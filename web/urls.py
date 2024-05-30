from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan-aptos/', views.scan_aptos, name='scan-aptos'),
    # path('/encontrado', views.scan_aptos, name='scan-aptos'),
    # path('/no-encontrado', views.scan_aptos, name='scan-aptos'),
    path('resultados/', views.resultados, name='resultados'),
]