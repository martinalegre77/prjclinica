from django.shortcuts import render

# Create your views here.

def index(request, template_name='web/index.html'):
    return render(request, template_name)


def scan_aptos(request, template_name='web/scan-aptos.html'):
    return render(request, template_name)


def resultados(request, template_name='web/resultados.html'):
    return render(request, template_name)