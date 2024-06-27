from django.shortcuts import redirect, render
# from django.http import Http404, HttpResponse
# import requests, sqlite3
from .forms import DeporteForm, DeportistaForm, InstitucionForm, UsuarioForm, EvaluacionForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required # para autenticacion
import re
from django.core.files.base import ContentFile
from django.contrib.auth import login, logout 
from django.views.decorators.csrf import csrf_protect
# from django.core.paginator import Paginator # paginación de html


############### FUNCIONES ######################
def comprobar_contrasena(password):
    may = False
    num = False
    if len(password) > 7:
        for  i in range(len(password)):
            if password[i].isupper():
                may = True
            if password[i].isnumeric():
                num = True
        if may and num:
            return True
        else: 
            return False
    else:
        return False


def validar_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return True
    else:
        return False


############### INDEX - LOGIN ######################
def index(request, template_name='main/index.html'):
    """ Página de inicio de la clínica"""
    return render(request, template_name)


def login_view(request, template_name='main/login.html'):
    """ Logín para entrar al sistema"""
    if request.method == 'GET':
        return render(request, template_name)
    else:
        try:
            user = Usuario.objects.get(username__exact = request.POST['username'], password__exact = request.POST['password'])
        except Usuario.DoesNotExist:
            user = request.POST['username']
            return redirect('not-found', user)
        else:
            if user.user_temp:
                return redirect('registro', id=user.pk)
            else:
                login(request, user)
                return redirect('menu')

        # Set a session value:
        #         request.session["user"] = user.username
        #         request.session["dni"] = user.password
        #         request.session['level'] = user.medico
        #         return redirect('registro')


def not_found(request, user, template_name='main/not-found.html'):
    """ Usuario no encontrado o datos mal cargados"""
    ctx = {'user': user}
    return render(request, template_name, ctx)

@csrf_protect
@login_required
def registro(request, id, template_name='main/registro.html'):
    """ Registro de usuarios """
    user = Usuario.objects.get(id = id)
    medico = user.medico
    if request.method == 'GET':
        form = UsuarioForm(instance=user)
        return render(request, template_name, {'form': form, 'medico': medico})
    else:
        errors = []
        form = UsuarioForm(request.POST, instance=user)
        # if form.is_valid():
            # print('Formulario válido')
        # Validación de datos
        if len(request.POST.get('nombres')) < 3 :
            errors.append('Ingrese un nombre válido')
        elif len(request.POST.get('apellido')) < 3 :
            errors.append('Ingrese un apellido válido')
        elif not comprobar_contrasena(request.POST.get('newpass')) :
            errors.append('La contraseña debe tener al menos una mayúscula, una minúscula, un número y ser de al menos 8 caracteres')
        elif not medico:
            # si no es médico guardo los datos
            try:
                Usuario.objects.filter(id=user.pk).update(password = request.POST.get('newpass'),
                                                            user_temp = False,
                                                            apellido = request.POST.get('apellido'),
                                                            nombres = request.POST.get('nombres')
                                                            )
                return redirect('re-login')
            except:
                errors.append('Ha ocurrido un error al intentar guardar los datos, intente nuevamente.')
        # si es médico sigo validando
        elif not request.POST.get('tipo_matricula'):
            errors.append('Debe seleccionar un tipo de matrícula')
        elif not request.POST.get('matricula') or len(request.POST.get('matricula')) < 4:
            print('Error de matricula')
            errors.append('Debe ingresar un número de matrícula válido')
        elif len(request.POST.get('especialidad')) < 6 :
            errors.append('Debe ingresar una especialidad válida')
        elif not validar_email(request.POST.get('mail')):
            errors.append('Debe ingresar una dirección de mail válida')
        elif not 'image' in request.FILES:
            errors.append('Debe tomarse una foto')
        else:
            image = request.FILES['image']
            try:
                user.image.save('foto.png', ContentFile(image.read()))
                Usuario.objects.filter(id=user.pk).update(password = request.POST.get('newpass'),
                                                                    user_temp = False,
                                                                    apellido = request.POST.get('apellido'),
                                                                    nombres = request.POST.get('nombres'),
                                                                    tipo_matricula = request.POST.get('tipo_matricula'),
                                                                    matricula = request.POST.get('matricula'),
                                                                    especialidad = request.POST.get('especialidad'),
                                                                    telefono = request.POST.get('telefono'),
                                                                    mail = request.POST.get('mail')
                                                                    )
                return redirect('re-login')
            except:
                errors.append('Ha ocurrido un error al intentar guardar los datos, intente nuevamente.')
        return render(request, template_name, {'form': form, 'medico': medico, 'errors': errors})


@csrf_protect
@login_required
def re_login(request, template_name='main/re-login.html'):
    """ Información registrada correctamente"""
    return render(request, template_name)


@csrf_protect
def cerrar_sesion(request):
    """Cerrar sesión (logout)"""
    logout(request)
    return redirect('login')


############### FUNCIONALIDAD APP ######################
@csrf_protect
@login_required
def menu(request, template_name='main/menu.html'):
    if request.method == 'POST':
        errors = []
        dni = request.POST.get('dni')
        if len(dni) < 8:
            errors.append('Debe ingresar un DNI válido.')
        else:
            return redirect('mostrar', dni)
        return render(request, template_name, {'errors': errors})
    else:
        # form = DeportistaForm()
        return render(request, template_name)


@csrf_protect
@login_required
def mostrar(request, dni, template_name='main/mostrar.html'):
    # paginator = Paginator()
    try:
        deportista = Deportista.objects.get(dni=dni)
        form = DeportistaForm(instance=deportista)
    except Deportista.DoesNotExist:
        deportista = None
        form = DeportistaForm()
    try:
        evaluaciones = Evaluacion.objects.filter(deportista=deportista)
    except Deportista.DoesNotExist:
        evaluaciones = None

    return render(request, template_name, {'form': form, 'dni': dni, 'deportista': deportista, 'evaluaciones': evaluaciones})


############### DEPORTISTA ######################
@csrf_protect
@login_required
def add_deportista(request, template_name='main/add-deportista.html'):
    """ Agregar Deportista"""
    if request.method == 'POST':
        form = DeportistaForm(request.POST)
        if form.is_valid():
            dni = request.POST.get('dni')
            form.save()
        return redirect('mostrar', dni)
    else:
        form = DeportistaForm()
    return render(request, template_name, {'form': form})


@csrf_protect
@login_required
def editar_deportista(request, id, template_name='main/add-deportista.html'):
    """ Editar Deportista"""
    form = DeportistaForm()
    error = None
    try:
        deportista = Deportista.objects.get(id=id)
        if request.method == 'GET':
            form = DeportistaForm(instance=deportista)
        else:
            form = DeportistaForm(request.POST, instance=deportista)
            if form.is_valid():
                dni = request.POST.get('dni')
                form.save()
            return redirect('mostrar', dni)
    except ObjectDoesNotExist as e: 
        error = 'No se encontraron datos del deportista'
    return render(request, template_name, {'form': form, 'error': error})

############### INSTITUCIONES ######################
@csrf_protect
@login_required
def listar_instituciones(request, template_name='main/list-instituciones.html'):
    """ Listar Instituciones"""
    instituciones = Institucion.objects.all()
    return render(request, template_name, {'instituciones': instituciones})

@csrf_protect
@login_required
def agregar_institucion(request, template_name='main/add-institucion.html'):
    """ Agregar Institucion"""
    if request.method == 'POST':
        form = InstitucionForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('listar-instituciones')
    else:
        form = InstitucionForm()
    return render(request, template_name, {'form': form})

@csrf_protect
@login_required
def editar_institucion(request, id, template_name='main/add-institucion.html'):
    """ Editar Institucion"""
    form = InstitucionForm()
    error = None
    try:
        institucion = Institucion.objects.get(id=id)
        if request.method == 'GET':
            form = InstitucionForm(instance=institucion)
        else:
            form = InstitucionForm(request.POST, instance=institucion)
            if form.is_valid():
                form.save()
            return redirect('listar-instituciones')
    except ObjectDoesNotExist as e: 
        error = 'No se encontró la institución deseada'
    return render(request, template_name, {'form': form, 'error': error})


############### DEPORTES ######################
@csrf_protect
@login_required
def listar_deportes(request, template_name='main/list-deportes.html'):
    """ Lista de Deportes"""
    deportes = Deporte.objects.all()
    return render(request, template_name, {'deportes': deportes})

@csrf_protect
@login_required
def agregar_deporte(request, template_name='main/add-deporte.html'):
    """ Agregar Deporte"""
    if request.method == 'POST':
        form = DeporteForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('listar-deportes')
    else:
        form = DeporteForm()
    return render(request, template_name, {'form': form})

@csrf_protect
@login_required
def editar_deporte(request, id, template_name='main/add-deporte.html'):
    """ Editar Deporte"""
    form = DeporteForm()
    error = None
    try:
        deporte = Deporte.objects.get(id=id)
        if request.method == 'GET':
            form = DeporteForm(instance=deporte)
        else:
            form = DeporteForm(request.POST, instance=deporte)
            if form.is_valid():
                form.save()
            return redirect('listar-deportes')
    except ObjectDoesNotExist as e: 
        error = 'No se encontró el deporte deseado'
    return render(request, template_name, {'form': form, 'error': error})