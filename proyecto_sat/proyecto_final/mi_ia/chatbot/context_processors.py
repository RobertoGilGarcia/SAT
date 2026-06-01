from .models import Conversacion, Mensaje, PerfilUsuario

def metricas_footer(request): # se utiliza en settings, para mostrar las métricas sin llamar explícitamente a la función
    conversaciones_totales = Conversacion.objects.count()
    mensajes_totales = Mensaje.objects.count()
    conversaciones_usuario = 0
    prompts_usuario = 0
    perfil_usuario = None
    tema_usuario = "claro"

    if request.user.is_authenticated:
        perfil_usuario, creado = PerfilUsuario.objects.get_or_create(usuario=request.user,defaults={'alias': request.user.username})

        conversaciones_usuario = Conversacion.objects.filter(usuario=request.user).count()
        prompts_usuario = Mensaje.objects.filter(conversacion__usuario=request.user,rol='user').count()

        tema_usuario = perfil_usuario.tema

    return {
        'conversaciones_totales': conversaciones_totales,
        'mensajes_totales': mensajes_totales,
        'conversaciones_usuario': conversaciones_usuario,
        'prompts_usuario': prompts_usuario,
        'perfil_usuario': perfil_usuario,
        'tema_usuario': tema_usuario,
    }