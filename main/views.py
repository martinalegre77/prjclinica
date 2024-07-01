import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import DeporteForm, DeportistaForm, InstitucionForm, UsuarioForm, EvaluacionForm
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required # para autenticacion
import re
from django.core.files.base import ContentFile
from django.contrib.auth import login, logout 
from django.views.decorators.csrf import csrf_protect
# import face_recognition
# Para QR y certificado
from PIL import Image 
from PIL import ImageDraw
from PIL import ImageOps 
from PIL import ImageFont 
from datetime import datetime
import time
import qrcode # libreria Qr


############### VARIABLES ######################

TIPO_APTO_CHOISE = {
    'A': 'APTO sin restricciones',
    'B': 'AUTORIZADO con recomendación de evaluación y/o tratamiento médico',
    'C': 'NO AUTORIZADO hasta completar la evaluación, tratamiento y/o rehabilitación'
}

TIPO_MATRICULA_CHOISE = {
    '1': 'M.N.',
    '2': 'M.P.'
}

DIR_REC = './media/recursos/' # carpeta para guardar las imágenes
DIR_CER = './media/certificados/' # carpeta para guardar las imágenes

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
    

def crear_qr(dni):
	# creamos el objeto qr
	qr = qrcode.QRCode(version=1, box_size=10, border=5) 
	qr.add_data(dni) # le pasamos los datos a convertir
	qr.make(fit=True) # creamos el código QR
	img = qr.make_image(fill='black', back_color='white') # creamos la imagen
	img.save(DIR_REC + f'QR_{dni}.png') # guardamos la imagen


def certificado_doc(apellido, nombres, dni, fecha_nac, apto, fecha_hoy, medico, matricula):
        # cargamos la imagen de fondo
        lienzo = Image.open(DIR_REC + 'apto_a.png')
        # objeto que usaremos para dibujar sobre el lienzo
        dibujo = ImageDraw.Draw(lienzo)
        # Apellido y nombres
        fuente = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=36, encoding='utf-8')
        texto_nombres = f'{apellido}, {nombres}'
        dibujo.text((330, 270), texto_nombres, font=fuente, fill='black')
        # DNI
        fuente = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=36, encoding='utf-8')
        texto_dni = f'{dni}'
        dibujo.text((130, 310), texto_dni, font=fuente, fill='black')
        # nacimiento
        fuente = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=36, encoding='utf-8')
        texto_nac = f'{fecha_nac}'
        dibujo.text((950, 310), texto_nac, font=fuente, fill='black')
        # apto
        fuente = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=60, encoding='utf-8')
        texto_apto = f'{apto}'
        dibujo.text((500, 1250), texto_apto, font=fuente, fill='black')
        # fecha
        fuente = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=36, encoding='utf-8')
        texto_fecha = f'{fecha_hoy}'
        dibujo.text((163, 1510), texto_fecha, font=fuente, fill='black')
        # medico
        fuente = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=36, encoding='utf-8')
        texto_medico = f'Dr/a {medico}'
        texto_mat = f'{matricula}'
        dibujo.text((1170, 1460), texto_medico, font=fuente, fill='black')
        dibujo.text((1205, 1490), texto_mat, font=fuente, fill='black')
        # QR
        # time.sleep(1)
        qr = Image.open(DIR_REC + f'QR_{dni}.png')
        # Eliminar el canal alfa 
        if qr.mode in ('RGBA', 'LA') or (qr.mode == 'P' and 'transparency' in qr.info):
            qr = qr.convert('RGB')
        qr_reescalado = qr.resize((308, 308), Image.Resampling.LANCZOS)
        qr_reescalado = ImageOps.contain(qr, (500, 500), Image.Resampling.LANCZOS) 
        lienzo.paste(qr_reescalado, (600, 600))
        # guardamos la imagen 
        lienzo.save(DIR_CER + f'certificado_{dni}.png')
        print('    Hecho')
        

# def reconocimiento(img1, img2):
#     # Cargar las imágenes a comparar
#     imagen1 = face_recognition.load_image_file("imagen1.jpg")
#     imagen2 = face_recognition.load_image_file("imagen2.jpg")

# # Obtener los encodings faciales de ambas imágenes
# encodings_imagen1 = face_recognition.face_encodings(imagen1)
# encodings_imagen2 = face_recognition.face_encodings(imagen2)

# if len(encodings_imagen1) == 0 or len(encodings_imagen2) == 0:
#     print("No se encontraron rostros en una de las imágenes.")
# else:
#     # Comparar los encodings faciales
#     if face_recognition.compare_faces(encodings_imagen1, encodings_imagen2)[0]:
#         print("Las fotos muestran a la misma persona.")
#     else:
#         print("Las fotos muestran a personas diferentes.")


# Función para convertir valores de formulario a booleanos
def to_bool(value):
    if value in ['true', 'True', '1', True]:
        return True
    elif value in ['false', 'False', '0', False]:
        return False
    elif value:
        return value
    else:
        return None


############### INDEX - LOGIN ######################
def index(request, template_name='main/index.html'):
    """ Página de inicio de la clínica"""
    return render(request, template_name)


def login_view(request, template_name='main/login.html'):
    """ Logín para entrar al sistema"""
    logout(request)
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
                login(request, user)
                return redirect('registro', id=user.pk)
            else:
                login(request, user)
                return redirect('menu')


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
    usuario = request.user
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

    return render(request, template_name, {'form': form, 'dni': dni, 'deportista': deportista, 'evaluaciones': evaluaciones, 'user': usuario})


@csrf_protect
@login_required
def evaluacion(request, id, template_name='main/evaluacion.html'):
    usuario = request.user
    deportista = Deportista.objects.get(id=id)

    if request.method == 'GET':
        form = EvaluacionForm()
        return render(request, template_name, {'form': form, 'user': usuario, 'deportista': deportista})
    else:
        form = EvaluacionForm(request.POST)
        errors = []
        required_fields = ['estado_general', 'talla', 'peso', 'presion_arterial', 'frecuencia_cardiaca', 'oxigeno_sangre']
        for field in required_fields:
            if not request.POST.get(field):
                errors.append(f'El campo {field.replace("_", " ").upper()} es obligatorio')
        # if not 'image' in request.FILES:
        #     errors.append('Debe tomarse una foto')
        # else:
        #     try:
        #         # Acá analiza las fotos
        #         image = request.FILES['image']
        #         # image_url = usuario.image.url
        #         # Llama a la función
        #         # if not match:
        #         # return redirect('error-reconocimiento', id)
        #     except:
        #         # No hay fotos
        #         return redirect('error-reconocimiento', id)
        if not errors:
            # Hace certificado
            fecha_actual = datetime.now()
            fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
            fecha_nacimiento = deportista.fecha_nac
            fecha_nac_formt = fecha_nacimiento.strftime("%d/%m/%Y")
            crear_qr(deportista.dni)
            for clave, valor in TIPO_APTO_CHOISE.items():
                if clave == request.POST.get('tipo'):
                    tipo_apto = valor
                    break
            for clave, valor in TIPO_MATRICULA_CHOISE.items():
                if clave == usuario.tipo_matricula:
                    tipo_mat = valor
                    break
            certificado_doc(deportista.apellido, deportista.nombres, deportista.dni, fecha_nac_formt, tipo_apto, 
                            fecha_formateada, f'{usuario.apellido}, {usuario.nombres}', f'{tipo_mat} {usuario.matricula}')
            # Grabar
            eval = Evaluacion(deportista = deportista, 
                                # FAMILIARES
                                fam_cardiovasculares = to_bool(request.POST.get('fam_cardiovasculares')),
                                fam_cardiovasculares_cual = to_bool(request.POST.get('fam_cardiovasculares_cual')),
                                fam_neurologicas = to_bool(request.POST.get('fam_neurologicas')),
                                fam_neurologicas_cual = to_bool(request.POST.get('fam_tumorales')),
                                fam_tumorales = to_bool(request.POST.get('fam_neurologicas_cual')),
                                fam_tumorales_cual = to_bool(request.POST.get('fam_tumorales_cual')),
                                fam_respiratorias = to_bool(request.POST.get('am_respiratorias')),
                                fam_respiratorias_cual = to_bool(request.POST.get('fam_respiratorias_cual')),
                                fam_desangre = to_bool(request.POST.get('fam_desangre')), 
                                fam_desangre_cual = to_bool(request.POST.get('fam_desangre_cual')),
                                fam_otras = to_bool(request.POST.get('fam_otras')),
                                fam_otras_cual = to_bool(request.POST.get('fam_otras_cual')),
                                fam_obs = to_bool(request.POST.get('fam_obs')),
                                # PERSONALES
                                per_cardiologica = to_bool(request.POST.get('per_cardiologica')),
                                per_cardiologica_cual = to_bool(request.POST.get('per_cardiologica_cual')),
                                per_respiratoria = to_bool(request.POST.get('per_respiratoria')),
                                per_respiratoria_cual = to_bool(request.POST.get('per_respiratoria_cual')),
                                per_neurologicas = to_bool(request.POST.get('per_neurologicas')),
                                per_neurologicas_cual = to_bool(request.POST.get('per_neurologicas_cual')),
                                per_infecciosas = to_bool(request.POST.get('per_infecciosas')),
                                per_infecciosas_cual = to_bool(request.POST.get('per_infecciosas_cual')),
                                per_cirugias = to_bool(request.POST.get('per_cirugias')),
                                per_cirugias_cual = to_bool(request.POST.get('per_cirugias_cual')),
                                per_alergias = to_bool(request.POST.get('per_alergias')),
                                per_alergias_cual = to_bool(request.POST.get('per_alergias_cual')),
                                per_traumatologicas = to_bool(request.POST.get('per_traumatologicas')),
                                per_traumatologicas_cual = to_bool(request.POST.get('per_traumatologicas_cual')),
                                per_otras = to_bool(request.POST.get('per_otras')),
                                per_otras_cual = to_bool(request.POST.get('per_otras_cual')),
                                # MEDICACIÓN
                                medicacion = to_bool(request.POST.get('medicacion')),
                                medicacion_cual = to_bool(request.POST.get('medicacion_cual')),
                                medicacion_dosis = to_bool(request.POST.get('medicacion_dosis')),
                                fuma = to_bool(request.POST.get('fuma')),
                                alcohol = to_bool(request.POST.get('alcohol')),
                                sustancias = to_bool(request.POST.get('sustancias')),
                                # EXAMEN FÍSICO
                                estado_general = request.POST.get('estado_general'),
                                talla = request.POST.get('talla'),
                                peso = request.POST.get('peso'),
                                presion_arterial = request.POST.get('presion_arterial'),
                                frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca'),
                                oxigeno_sangre = request.POST.get('oxigeno_sangre'),
                                # CERTIFICADO DE APTO FISICO
                                medico = usuario,
                                tipo = tipo_apto,
                                observaciones = request.POST.get('observaciones'))                    
            eval.save()
            # Guardo certificado
            ruta = DIR_CER + f'certificado_{deportista.dni}.png'
            with open(ruta, 'rb') as f:
                image = ContentFile(f.read())
            eval.certificado_file.save(f'certificado_{deportista.dni}.png', ContentFile(image.read()))
            return redirect('guardado')
        else:
            return render(request, template_name, {'form': form, 'errors': errors, 'deportista': deportista})


@csrf_protect
@login_required
def guardado(request, template_name='main/guardado.html'):
    return render(request, template_name)


@csrf_protect
@login_required
def error_reconocimiento(request, id, template_name='error_reconocimiento.html'):
    return render(request, template_name, {'user_id': id})


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