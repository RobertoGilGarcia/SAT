from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import PromptForm
from .utils import llamar_ia_nvidia

def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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

def cerrar_sesion(request):
    logout(request)
    return redirect('home')