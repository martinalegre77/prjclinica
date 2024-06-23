from django.urls import include, path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'), # ingreso a la app
    path('cerrar-sesion', views.cerrar_sesion, name='cerrar-sesion'), # cerrar sesión
    path('not-found/<str:user>', views.not_found, name='not-found'), # usuario no encontrado
    path('registro/<int:id>', login_required(views.registro), name='registro'), # registro de nuevo usuario
    path('menu/', login_required(views.menu), name='menu'), # menu de la app
    path('mostrar-datos/<int:id>/<str:dni>', views.mostrar_datos, name='mostrar-datos'), # muestra la consulta
    path('realizar-apto/', views.realizar_apto, name='realizar-apto'),
    path('re-login/', login_required(views.re_login), name='re-login'), # redireccionamiento a login
    path('list-instituciones/', login_required(views.listar_instituciones), name='listar-instituciones'), # listar instituciones
    path('add-institucion/', login_required(views.agregar_institucion), name='agregar-institucion'), # agregrar institución
    path('edit-institucion/<int:id>/', login_required(views.editar_institucion), name='editar-institucion'), # editar info institución
    path('list-deportes/', login_required(views.listar_deportes), name='listar-deportes'), # lista de deportes
    path('add-deporte/', login_required(views.agregar_deporte), name='agregar-deporte'), # agregar deporte
    path('edit-deporte/<int:id>/', login_required(views.editar_deporte), name='editar-deporte'), # editar info deporte
    # path('accounts/', include('django.contrib.auth.urls')), # para autenticacion
]