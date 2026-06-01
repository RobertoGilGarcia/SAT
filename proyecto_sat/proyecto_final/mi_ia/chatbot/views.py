from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .forms import PromptForm, PerfilUsuarioForm
from .utils import llamar_ia_nvidia, crear_titulo_conversacion, convertir_markdown_a_html, preparar_mensajes_para_html, construir_historial_conversacion
from .models import PerfilUsuario, Conversacion, Mensaje


def obtener_metricas_usuario(request):
    conversaciones_totales = Conversacion.objects.count()
    mensajes_totales = Mensaje.objects.count()
    conversaciones_usuario = 0
    prompts_usuario = 0

    if request.user.is_authenticated:
        conversaciones_usuario = Conversacion.objects.filter(usuario=request.user).count()
        prompts_usuario = Mensaje.objects.filter(
            conversacion__usuario=request.user,
            rol='user'
        ).count()

    return {
        'conversaciones_totales': conversaciones_totales,
        'mensajes_totales': mensajes_totales,
        'conversaciones_usuario': conversaciones_usuario,
        'prompts_usuario': prompts_usuario,
    }


def home(request):
    respuesta = None
    respuesta_html = None
    prompt_usuario = None

    if request.method == 'POST':
        form = PromptForm(request.POST)

        if form.is_valid():
            prompt_usuario = form.cleaned_data['prompt']
            mensajes = [
                {
                    "role": "user",
                    "content": prompt_usuario
                }
            ]
            respuesta = llamar_ia_nvidia(mensajes)
            respuesta_html = convertir_markdown_a_html(respuesta)
    else:
        form = PromptForm()

    return render(request, 'home.html', {
        'form': form,
        'respuesta': respuesta,
        'respuesta_html': respuesta_html,
        'prompt_usuario': prompt_usuario,
    })


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # formulario de registro propio de django

        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(usuario=user)
            login(request, user)
            return redirect('cuenta')
    else:
        form = UserCreationForm() # crea el formulario vacío para que el usuario pueda rellenarlo

    return render(request, 'registro.html', {
        'form': form
    })


@login_required
def cuenta(request):
    conversaciones = Conversacion.objects.filter(usuario=request.user).order_by('-fecha_actualizacion', '-id')

    conv_id = request.GET.get('conv_id')

    if conv_id:
        conversacion = get_object_or_404(
            Conversacion,
            id=conv_id,
            usuario=request.user
        )
    else:
        conversacion = conversaciones.first()

    form = PromptForm()

    if conversacion:
        mensajes = preparar_mensajes_para_html(
            conversacion.mensajes.order_by('id')
        )
    else:
        mensajes = []

    return render(request, 'cuenta.html', {
        'form': form,
        'conversaciones': conversaciones,
        'conversacion_activa': conversacion,
        'mensajes': mensajes,
    })


@login_required
def iniciar_conversacion(request):
    if request.method == 'POST':
        form = PromptForm(request.POST)

        if form.is_valid():
            prompt_usuario = form.cleaned_data['prompt']
            titulo = crear_titulo_conversacion(prompt_usuario)

            conversacion = Conversacion.objects.create(usuario=request.user,titulo=titulo)

            Mensaje.objects.create(conversacion=conversacion,rol='user',contenido=prompt_usuario)

            historial = construir_historial_conversacion(conversacion)
            respuesta = llamar_ia_nvidia(historial)

            Mensaje.objects.create(conversacion=conversacion,rol='assistant',contenido=respuesta)

            conversaciones = Conversacion.objects.filter(usuario=request.user).order_by('-fecha_actualizacion', '-id')

            mensajes = preparar_mensajes_para_html(conversacion.mensajes.order_by('id'))

            contexto = {
                'form': PromptForm(),
                'conversaciones': conversaciones,
                'conversacion_activa': conversacion,
                'mensajes': mensajes,
                'actualizar_footer': True,
            }

            contexto.update(obtener_metricas_usuario(request))

            if request.headers.get('HX-Request'):
                response = render(request, 'cuenta_contenido.html', contexto)
                response['HX-Push-Url'] = reverse('cuenta') + f'?conv_id={conversacion.id}'
                return response

            return redirect(f"{reverse('cuenta')}?conv_id={conversacion.id}")

    return redirect('cuenta')


@login_required
def configuracion_cuenta(request, nombre):
    if nombre != request.user.username:
        return redirect('configuracion', nombre=request.user.username)

    perfil, creado = PerfilUsuario.objects.get_or_create(usuario=request.user,defaults={'alias': request.user.username})

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST,instance=perfil)

        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            return redirect('configuracion', nombre=request.user.username)
    else:
        form = PerfilUsuarioForm(instance=perfil)
        form.fields['email'].initial = request.user.email

    return render(request, 'configuracion.html', {'form': form,'perfil': perfil,})


@login_required
def crear_conversacion(request):
    if request.method == 'POST':
        nueva_conv = Conversacion.objects.create(usuario=request.user,titulo='Nueva conversación')
        return redirect(f"{reverse('cuenta')}?conv_id={nueva_conv.id}")

    return redirect('cuenta')


def cerrar_sesion(request):
    logout(request)
    return redirect('home')


@login_required
def borrar_conversacion(request, conv_id):
    if request.method == 'POST':
        conversacion = get_object_or_404(Conversacion,id=conv_id,usuario=request.user)
        conversacion.delete()

    return redirect('cuenta')


@login_required
def actualizar_mensajes(request, conv_id):
    conversacion = get_object_or_404(Conversacion,id=conv_id,usuario=request.user) #coges la conversacion actual con su id

    if request.method == 'POST':
        form = PromptForm(request.POST) # ves lo que hay en el POST (el prompt del usuario)

        if form.is_valid():
            prompt_usuario = form.cleaned_data['prompt']

            if conversacion.titulo == 'Nueva conversación': # al crear una conversacion nueva, el titulo generico es este, pues lo cambias si lo es
                nuevo_titulo = crear_titulo_conversacion(prompt_usuario)
                conversacion.titulo = nuevo_titulo
                conversacion.save()

            Mensaje.objects.create(conversacion=conversacion,rol='user',contenido=prompt_usuario) # creas el objeto mensaje para la bbdd

            historial = construir_historial_conversacion(conversacion)
            respuesta = llamar_ia_nvidia(historial)

            Mensaje.objects.create(conversacion=conversacion,rol='assistant',contenido=respuesta) # guardas la respuesta generada

    conversaciones = Conversacion.objects.filter(usuario=request.user).order_by('-fecha_actualizacion', '-id')

    mensajes = preparar_mensajes_para_html(conversacion.mensajes.order_by('id')) # parseas los mensajes para que se vean bonitos formato markdown

    contexto = {
        'form': PromptForm(),
        'conversaciones': conversaciones,
        'conversacion_activa': conversacion,
        'mensajes': mensajes,
        'actualizar_footer': True,
    }

    contexto.update(obtener_metricas_usuario(request)) # actualizas el footer

    if request.headers.get('HX-Request'): # si viene de HTMX actualizas solo el footer y los mensajes
        return render(request, 'cuenta_contenido.html', contexto)

    return redirect(f"{reverse('cuenta')}?conv_id={conversacion.id}") # redirige a la URL de esa conversacion en especifico


@login_required
def conversacion_json(request, conv_id):
    conversacion = get_object_or_404(Conversacion,id=conv_id,usuario=request.user) #coges los datos de la conversacion

    mensajes = conversacion.mensajes.order_by('id')

    datos = {
        'id': conversacion.id,
        'titulo': conversacion.titulo,
        'usuario': request.user.username,
        'fecha_creacion': conversacion.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_actualizacion': conversacion.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S'),
        'total_mensajes': mensajes.count(),
        'mensajes': []}

    for mensaje in mensajes:
        datos['mensajes'].append({'id': mensaje.id,'rol': mensaje.rol,'contenido': mensaje.contenido,'fecha_creacion': mensaje.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')})

    return JsonResponse(datos, json_dumps_params={'ensure_ascii': False,'indent': 4})


def ayuda(request):
    return render(request, 'ayuda.html')


def error_404(request, exception):
    return render(request, '404.html', {'path': request.path}, status=404)