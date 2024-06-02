from django.shortcuts import redirect, render
# from django.http import Http404, HttpResponse
# import requests, sqlite3
from .forms import DeporteForm, DeportistaForm, InstitucionForm, UsuarioForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import login_required # para autenticacion
import re

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


def index(request, template_name='main/index.html'):
    """ Página de inicio de la clínica"""
    return render(request, template_name)
    

def login(request, template_name='main/login.html'):
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
                return redirect('consultar')

        # Set a session value:
        #         request.session["user"] = user.username
        #         request.session["dni"] = user.password
        #         request.session['level'] = user.medico
        #         return redirect('registro')
        

def not_found(request, user, template_name='main/not-found.html'):
    """ Usuario no encontrado o datos mal cargados"""
    ctx = {'user': user}
    return render(request, template_name, ctx)


# @login_required
def registro(request, id, template_name='main/registro.html'):
    """ Registro de usuarios """
    user = Usuario.objects.get(id = id)
    medico = user.medico
    if request.method == 'GET':
        print('GET')
        form = UsuarioForm(instance=user)
        return render(request, template_name, {'form': form, 'medico': medico})
    else:
        print('POST')
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
            print('No es medico')
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
        else:
            try:
                print('Intentando grabar')
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


# @login_required
def consultar(request, template_name='main/consultar.html'):
    if request.method == 'POST':
        deportista = Deportista.objects.filter(dni=request.POST.get('dni'))
        form = DeportistaForm(instance=deportista)
        print(deportista)

        return render(request, template_name, {'form': form})
    else:
        form = DeportistaForm()
        return render(request, template_name)
    

# @login_required
def ingresar_datos(request):
    pass


# @login_required
def realizar_apto(request, template_name='main/realizar-apto.html'):
    form = UsuarioForm() # borrar cuando esté completo
    ctx = {'form': form}
    return render(request, template_name, ctx)
    # return render(request, template_name)


def re_login(request, template_name='main/re-login.html'):
    """ Información registrada correctamente"""
    return render(request, template_name)


############### INSTITUCIONES ######################
def listar_instituciones(request, template_name='main/list-instituciones.html'):
    """ Listar Instituciones"""
    instituciones = Institucion.objects.all()
    return render(request, template_name, {'instituciones': instituciones})


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
def listar_deportes(request, template_name='main/list-deportes.html'):
    """ Lista de Deportes"""
    deportes = Deporte.objects.all()
    return render(request, template_name, {'deportes': deportes})


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




# -------------------------------------------------------------------------------#


# def scan_aptos(request, template_name='main/scan-aptos.html'):
#     return render(request, template_name)


# def aptos_fisicos(request, template_name='main/aptos-fisicos.html'):
#     if request.method == 'POST':
#         form = AptoForm(request.POST)
#         if form.is_valid():
#             conn = sqlite3.connect('contabilidad.sqlite') # conexion a la db
#             cursor = conn.cursor() # crea un cursor para recorrer la db
#             cursor.execute('INSERT INTO personas VALUES (?, ?)',
#                         (form.cleaned_data['nombre'], form.cleaned_data['edad'])) # ejecutamos codigo sql
#             conn.commit()
#             conn.close()
#             # return HttpResponse('Cliente cargado correctamente')
#             return redirect('clientes') 
#     else:
#         form = AptoForm()
    
#     data = {'form': form}                                  
#     return render(request, template_name, data)


# def primer_apto(request, template_name='main/primer-apto.html'):
#     return render(request, template_name)


# def nuevo_apto(request, template_name='main/nuevo-apto.html'):
#     return render(request, template_name)


#######################################################################


# def certificado(request):
#     """Concultar una API"""
#     r = requests.get("https://rickandmortyapi.com/api/character/520")
#     if r.status_code == 200:
#         contenido = r.json()
#         html = f"""
#                         <html>
#                         <title>Personajes THE RICK AND MORTY</title>
#                         <p><strong>Nombre del Personaje: </strong>{contenido['name']}</p>    
#                         <p><strong>Especie del Personaje: </strong>{contenido['species']}</p>
#                         </html>
#                 """ 
#     else:
#         html = "Error, no se pudo obtener la información"

#     return HttpResponse(html)


# def clientes(request, template_name='main/clientes.html'):
#     conn = sqlite3.connect('contabilidad.sqlite') # conecta a la base de datos
#     cliente = conn.cursor() # crea un cursor para recorrer la base de datos
#     cliente.execute('select nombre, edad from personas') # a traves del cursor ejecutamos codigo sql
#     cliente_list = cliente.fetchall()
#     conn.close()
#     dato = {'clientes': cliente_list}
#     return render(request, template_name, dato)


# def cliente(request, nombre_cliente, template_name='main/cliente.html'):
#     conn = sqlite3.connect('contabilidad.sqlite') # conecta a la base de datos
#     cursor = conn.cursor() # crea un cursor para recorrer la base de datos
#     cursor.execute('SELECT nombre, edad FROM personas WHERE nombre=?', [nombre_cliente]) # a traves del cursor ejecutamos codigo sql
#     cliente = cursor.fetchone()
#     # capturamos el error si no hay resultados
#     if cliente is None:
#         raise Http404
#     dato = {'cliente': cliente}
#     return render(request, template_name, dato)
