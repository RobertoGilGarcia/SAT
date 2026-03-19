from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contenido

# Create your views here.
def index(request):
    return HttpResponse("<h1>Aplicacion de contenido CMS<h1>") #respuesta http

@csrf_exempt
def get_content(request, llave):
    if request.method == "PUT":
        nuevo_contenido = request.body.decode('utf-8')
        Contenido.objects.update_or_create(clave=llave, defaults={'valor': nuevo_contenido})
    try:
        respuesta = Contenido.objects.get(clave=llave).valor
    except Contenido.DoesNotExist:
        respuesta = 'No existe contenido para la clave ' + llave
    return HttpResponse(respuesta)