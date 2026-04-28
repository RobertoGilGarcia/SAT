from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import PromptForm
from .utils import llamar_ia_nvidia
from .models import PerfilUsuario
from .forms import PerfilUsuarioForm

def home(request):
    respuesta = None
    prompt_usuario = None

    if request.method == 'POST':
        form = PromptForm(request.POST)

        if form.is_valid():
            prompt_usuario = form.cleaned_data['prompt']
            respuesta = llamar_ia_nvidia(prompt_usuario)
    else:
        form = PromptForm()

    return render(request, 'home.html', {
        'form': form,
        'respuesta': respuesta,
        'prompt_usuario': prompt_usuario,
    })

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(user=user)
            login(request, user)
            return redirect('cuenta')
    else:
        form = UserCreationForm()

    return render(request, 'registro.html', {'form': form})

@login_required
def cuenta(request):
    respuesta = None
    prompt_usuario = None

    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt_usuario = form.cleaned_data['prompt']
            respuesta = llamar_ia_nvidia(prompt_usuario)
    else:
        form = PromptForm()

    return render(request, 'cuenta.html', {
        'form': form,
        'respuesta': respuesta,
        'prompt_usuario': prompt_usuario,
    })


@login_required
def configuracion_cuenta(request, nombre):
    # Si alguien intenta acceder a la configuración de otro usuario,
    # lo redirigimos a su propia configuración.
    if nombre != request.user.username:
        return redirect('configuracion', nombre=request.user.username)
    # Cogemos el perfil asociado al usuario conectado.
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilUsuarioForm(
            request.POST,
            request.FILES,
            instance=perfil
        )
        if form.is_valid():
            form.save()
            return redirect('cuenta')
    else:
        form = PerfilUsuarioForm(instance=perfil)
    return render(request, 'configuracion.html', {
        'form': form,
        'perfil': perfil,
    })

def cerrar_sesion(request):
    logout(request)
    return redirect('home')