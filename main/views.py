from .models import *
from .forms import DeporteForm, DeportistaForm, InstitucionForm, UsuarioForm, EvaluacionForm

from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required # para autenticacion
from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.contrib.auth import login, logout, update_session_auth_hash 
from django.views.decorators.csrf import csrf_protect

# Para validar mail
import re

# Para convertir datos del formulario
from decimal import Decimal, InvalidOperation

# Para certificado
from PIL import Image 
from PIL import ImageDraw
from PIL import ImageOps 
from PIL import ImageFont

# Para Qr
import qrcode 

# Para cambiar zona horaria 
from django.utils import timezone

# Para reconocimiento facial
import cv2
import face_recognition


# VARIABLES
TIPO_APTO_CHOISE = {
    'A': 'APTO sin restricciones',
    'B': 'AUTORIZADO con recomendación de evaluación y/o tratamiento médico',
    'C': 'NO AUTORIZADO hasta completar la evaluación, tratamiento y/o rehabilitación'
}

LEYENDA = {
    'A': ['APTO', ''],
    'B': ['AUTORIZADO', 'con recomendación de evaluación y/o tratamiento médico'],
    'C': ['NO AUTORIZADO', 'hasta completar la evaluación, tratamiento y/o rehabilitación']
}


TIPO_MATRICULA_CHOISE = {
    '1': 'M.N.',
    '2': 'M.P.'
}

DIR_REC = './media/recursos/' # carpeta de recursos de imágenes
DIR_CER = './media/certificados/' # carpeta para guardar los certificados
DIR_FAC = './media/images/' # carpeta para guardar las fotos de reconocimiento


# FUNCIONES 
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
        texto_dni = f'{format_dni(dni)}'
        dibujo.text((130, 310), texto_dni, font=fuente, fill='black')
        # nacimiento
        fuente = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=36, encoding='utf-8')
        texto_nac = f'{fecha_nac}'
        dibujo.text((950, 310), texto_nac, font=fuente, fill='black')
        # apto
        fuente1 = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=60, encoding='utf-8')
        texto_apto_1 = f'{LEYENDA[apto][0]}'
        bbox1 = dibujo.textbbox((0, 0), texto_apto_1, font=fuente1)
        ancho1 = bbox1[2] - bbox1[0]
        dibujo.text((850 - ancho1//2, 1220), texto_apto_1, font=fuente1, fill='black')
        fuente2 = ImageFont.truetype(DIR_REC + 'UbuntuMono-Bold.ttf', size=48, encoding='utf-8')
        texto_apto_2 = f'{LEYENDA[apto][1]}'
        bbox2 = dibujo.textbbox((0, 0), texto_apto_2, font=fuente2)
        ancho2 = bbox2[2] - bbox2[0]
        dibujo.text((850 - ancho2//2, 1300), texto_apto_2, font=fuente2, fill='black')
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
        qr = Image.open(DIR_REC + f'QR_{dni}.png')
        # Eliminar el canal alfa 
        if qr.mode in ('RGBA', 'LA') or (qr.mode == 'P' and 'transparency' in qr.info):
            qr = qr.convert('RGB')
        qr_reescalado = qr.resize((308, 308), Image.Resampling.LANCZOS)
        qr_reescalado = ImageOps.contain(qr, (500, 500), Image.Resampling.LANCZOS) 
        lienzo.paste(qr_reescalado, (600, 600))
        # guardamos la imagen 
        lienzo.save(DIR_CER + f'certificado_{dni}.png')


def reconocimiento(img):
    # leer imagenes
    image1 = cv2.imread(DIR_FAC + 'reconocimiento.png')
    image2 = cv2.imread(img)
    # reconocer rostros
    face1 = face_recognition.face_locations(image1)[0]
    face2 = face_recognition.face_locations(image2)[0]
    # obtener los encodings faciales de ambas imágenes
    face1_enc = face_recognition.face_encodings(image1, known_face_locations=[face1])[0]
    face2_enc = face_recognition.face_encodings(image2, known_face_locations=[face2])[0]
    # comprobar si hay rostros en las imágenes
    if len(face1_enc) == 0 or len(face2_enc) == 0:
        # No hay rostros
        return False
    else:
        # compara los rostros
        resultado = face_recognition.compare_faces([face1_enc], face2_enc) 
        if resultado[0]:
            # Las fotos muestran a la misma persona
            return True
        else:
            # Las fotos muestran a personas diferentes
            return False


# Convertir valores de formulario a booleanos
def to_bool(value):
    if value in ['true', 'True', '1', True]:
        return True
    elif value in ['false', 'False', '0', False]:
        return False
    elif value:
        return value
    else:
        return None
    

# Formateo de número de DNI (agregar puntos)
def format_dni(dni):
    numero = int(dni)
    format = f"{numero:,}".replace(",", ".") 
    return format 


# VISTAS # GENERALES 

def index(request, template_name='main/index.html'):
    """ Página de inicio de la clínica"""
    logout(request)
    return render(request, template_name)


def login_view(request, template_name='main/login.html'):
    """ Logín para entrar al sistema"""
    logout(request)

    if request.method == 'GET':
        return render(request, template_name)
    else:
        # method = POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Buscar el usuario en la base de datos
            user = Usuario.objects.get(username=username)
            
            # Comprobar si la contraseña ingresada coincide con la encriptada
            if check_password(password, user.password):

                # Iniciar sesión si las contraseñas coinciden
                login(request, user)
                return redirect('menu')
            
                # Iniciar sesión si las contraseñas (formato plano) coinciden
            elif password == user.password and not user.user_temp:
                login(request, user)
                return redirect('menu')
            
                # Ir al registro si la contraseña no está encriptada
            elif password == user.password and user.user_temp:
                login(request, user)
                return redirect('registro', id=user.pk)        
            
                # Ir a usuario no encontrado si hay error
            else:
                return redirect('not-found', username)
            
        except Usuario.DoesNotExist:

            # Ir a usuario no encontrado
            return redirect('not-found', username)


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
        return render(request, template_name, {'form': form, 
                                                'medico': medico, 
                                                'post_method': False})
    
    if request.method == 'POST':
        errors = []
        form = UsuarioForm(request.POST)

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
                user.set_password(request.POST.get('newpass'))
                user.apellido = request.POST.get('apellido')
                user.nombres = request.POST.get('nombres')
                user.user_temp = False
                
                user.save()

                # mantenerlo logueado al usuario 
                update_session_auth_hash(request, user)

                # Redireccionamiento
                return redirect('re-login')

            except Exception as e:
                errors.append(f'Ha ocurrido un error al intentar guardar los datos, intente nuevamente: {str(e)}.')

        # si es médico valido campos adicionales
        elif not request.POST.get('tipo_matricula'):
            errors.append('Debe seleccionar un tipo de matrícula')
        elif not request.POST.get('matricula') or len(request.POST.get('matricula')) < 4:
            errors.append('Debe ingresar un número de matrícula válido')
        elif len(request.POST.get('especialidad')) < 6 :
            errors.append('Debe ingresar una especialidad válida')
        elif not validar_email(request.POST.get('mail')):
            errors.append('Debe ingresar una dirección de mail válida')
        
        elif 'image' not in request.FILES:
            errors.append('Debe tomarse una foto')

        # Si no hay errores, guardar los datos del médico
        else:
            image = request.FILES['image']
            try:
                user.image.save('foto.png', ContentFile(image.read()))

                # Guardar contraseña cifrada y otros datos del médico
                user.set_password(request.POST.get('newpass'))
                user.apellido = request.POST.get('apellido')
                user.nombres = request.POST.get('nombres')
                user.tipo_matricula = request.POST.get('tipo_matricula')
                user.matricula = request.POST.get('matricula')
                user.especialidad = request.POST.get('especialidad')
                user.telefono = request.POST.get('telefono')
                user.mail = request.POST.get('mail')
                user.user_temp = False
                
                user.save()

                # mantenerlo logueado al usuario 
                update_session_auth_hash(request, user)

                # Redireccionamiento
                return redirect('re-login')
            
            except Exception as e:
                errors.append(f'Ha ocurrido un error al intentar guardar los datos, intente nuevamente: {str(e)}.')
        
        # # Si hay errores, renderizar nuevamente el formulario
        return render(request, template_name, {'errors': errors,
                                                'form': form, 
                                                'medico': medico,
                                                'post_method': True 
                                                })
    

@csrf_protect
@login_required
def re_login(request, template_name='main/re-login.html'):
    """ Información registrada correctamente"""
    # logout(request)
    return render(request, template_name)


@csrf_protect
def cerrar_sesion(request):
    """Cerrar sesión (logout)"""
    logout(request)
    return redirect('login')


# VISTAS # FUNCIONALES

@csrf_protect
@login_required
def menu(request, template_name='main/menu.html'):
    if request.method == 'POST':
        errors = []
        dni = request.POST.get('dni')
        if not dni.isdecimal():
            errors.append('Debe ingresar sólo números, sin puntos')
        elif len(dni) != 8:  
            errors.append('Debe ingresar un DNI válido')
        else:
            return redirect('mostrar', dni)
        return render(request, template_name, {'errors': errors})
    else:
        return render(request, template_name)


@csrf_protect
@login_required
def mostrar(request, dni, template_name='main/mostrar.html'):
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

    return render(request, template_name, {'form': form, 
                                            'dni': format_dni(dni), 
                                            'deportista': deportista, 
                                            'evaluaciones': evaluaciones, 
                                            'user': usuario})


@csrf_protect
@login_required
def evaluacion(request, id, template_name='main/evaluacion.html'):
    usuario = request.user
    deportista = Deportista.objects.get(id=id)
    errors = []

    # Si el método es GET
    if request.method == 'GET':
        form = EvaluacionForm()
        return render(request, template_name, {'form': form, 
                                                'user': usuario, 
                                                'deportista': deportista, 
                                                'dni': format_dni(deportista.dni), 
                                                'post_method': False})
    
    # Si el método es POST
    else:
        form = EvaluacionForm(request.POST)

        if not request.POST.get('estado_general'):
            errors.append('El campo "Estado General" es obligatorio')
        elif not request.POST.get('presion_arterial'):
            errors.append('El campo "Presión Arterial" es obligatorio')
        elif not request.POST.get('frecuencia_cardiaca'):
            errors.append('El campo "Frecuencia Cardíaca" es obligatorio')
        elif not 'image' in request.FILES:
            errors.append('Debe tomarse una foto')
        elif not request.POST.get('observaciones'):
            errors.append('El campo Observaciones es obligatorio')
        else:
        # pasar a decimal talla, peso y oxígeno
            try:
                talla = Decimal(request.POST.get('talla'))
                if talla < 1 or  talla > 2.4:
                    errors.append('Debe ingresar la altura en metros utilizando el punto decimal para los centimetros')
            except InvalidOperation:
                errors.append('Debe ingresar la altura en metros utilizando el punto decimal para los centimetros')
            try:
                peso = Decimal(request.POST.get('peso'))
                if peso < 30 or  peso > 150:
                    errors.append('Debe ingresar el peso en kilogramos utilizando el punto decimal para los gramos')
            except InvalidOperation:
                errors.append('Debe ingresar el peso en kilogramos utilizando el punto decimal para los gramos')
            try:
                oxigeno = int(request.POST.get('oxigeno_sangre'))
                if oxigeno < 75 or  oxigeno > 100:
                    errors.append('Debe ingresar la saturación de oxígeno utilizando solo números')
            except InvalidOperation:
                errors.append('Debe ingresar la saturación de oxígeno utilizando solo números')

        # NO hay errores
        if not errors:
            try:
                # manejo de imagenes
                image_file = request.FILES['image']
                image_fc = Image.open(image_file)
                image_fc.save(DIR_FAC + 'reconocimiento.png')
                image_path = usuario.image.path    
                if not reconocimiento(image_path):
                    print("No es la misma persona")
                    return redirect('error-reconocimiento', id)
            except Exception as e:
                print("Error en el reconocimiento")
                return redirect('error-reconocimiento', id)
            
            # Si el reconocimiento es true hace el certificado
            fecha_actual = timezone.now()
            fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
            fecha_nacimiento = deportista.fecha_nac
            fecha_nac_formt = fecha_nacimiento.strftime("%d/%m/%Y")
            crear_qr(deportista.dni)
            
            for clave, valor in TIPO_APTO_CHOISE.items():
                if clave == request.POST.get('tipo'):
                    leyenda_apto = clave
                    break
            
            for clave, valor in TIPO_MATRICULA_CHOISE.items():
                if clave == usuario.tipo_matricula:
                    tipo_mat = valor
                    break
            
            certificado_doc(deportista.apellido, deportista.nombres, deportista.dni, fecha_nac_formt, leyenda_apto, 
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
                                tipo = request.POST.get('tipo'),
                                # fecha = fecha_actual,
                                observaciones = request.POST.get('observaciones'))                    
            eval.save()
            # Guardo certificado
            ruta = DIR_CER + f'certificado_{deportista.dni}.png'
            with open(ruta, 'rb') as f:
                image = ContentFile(f.read())
            eval.certificado_file.save(f'certificado_{deportista.dni}.png', ContentFile(image.read()))
            return redirect('guardado')

        # HAY errores
        else:
            print("Hay errores")
            print(errors)
            return render(request, template_name, {'form': form, 
                                                    'user': usuario, 
                                                    'deportista': deportista,
                                                    'dni': format_dni(deportista.dni), 
                                                    'errors': errors, 
                                                    'post_method': True})


@csrf_protect
@login_required
def guardado(request, template_name='main/guardado.html'):
    return render(request, template_name)


@csrf_protect
@login_required
def error_reconocimiento(request, id, template_name='main/error-reconocimiento.html'):
    usuario = request.user
    return render(request, template_name, {'usuario': usuario, 'deportista_id': id})


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