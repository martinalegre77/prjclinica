from django.http import JsonResponse
from django.shortcuts import redirect, render
from main.models import Deportista, Evaluacion

# VARIABLES
TIPO_APTO_CHOISE = {
    'A': 'APTO sin restricciones',
    'B': 'AUTORIZADO con recomendación de evaluación y/o tratamiento médico',
    'C': 'NO AUTORIZADO hasta completar la evaluación, tratamiento y/o rehabilitación'
}

# VIEWS
def index(request, template_name='web/index.html'):
    return render(request, template_name)


def scan_aptos(request, template_name='web/scan-aptos.html'):
    return render(request, template_name)


def consulta_deportista(request, qr, template_name='web/consulta-deportista.html'):
    if request.method == 'GET':
        tipo_apto = ''
        # codigo_qr = request.GET.get('codigo_qr')  
        try:
            deportista = Deportista.objects.get(dni=qr)
            evaluacion = Evaluacion.objects.filter(deportista=deportista).latest('fecha')
            fecha_nacimiento = deportista.fecha_nac
            fecha_nac_formt = fecha_nacimiento.strftime("%d/%m/%Y")
            fecha_eval = evaluacion.fecha
            fecha_eval_formt = fecha_eval.strftime("%d/%m/%Y")
            data = {
                'nombre': deportista.nombres,
                'apellido': deportista.apellido,
                'edad': deportista.edad,
                'dni': deportista.dni,
                'nac': fecha_nac_formt,
                'fecha': fecha_eval_formt,
                'apto': evaluacion.tipo
            }
            return render(request, template_name, data)
        except Deportista.DoesNotExist:
            return redirect('no-encontrado', qr)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def no_encontrado(request, qr, template_name='web/no-encontrado.html'):
    """ Deportista no encontrado"""
    return render(request, template_name, {'qr': qr})