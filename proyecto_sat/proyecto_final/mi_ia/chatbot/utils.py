import os
import requests
import markdown
from django.utils.html import escape


def llamar_ia_nvidia(mensajes_historial):
    """
    Envía a NVIDIA una lista de mensajes con formato:
    [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."},
        {"role": "user", "content": "..."}
    ]

    En las conversaciones privadas se le pasa el historial completo.
    En la prueba gratuita se le pasa solo el prompt actual.
    """
    api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        return "Error: no se ha configurado la variable de entorno NVIDIA_API_KEY."

    url = "https://integrate.api.nvidia.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "google/gemma-2-2b-it",
        "messages": mensajes_historial,
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 512,
        "stream": False,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return f"Error en la API: {response.status_code} - {response.text}"

        data = response.json()
        respuesta = data["choices"][0]["message"]["content"]
        return respuesta

    except requests.exceptions.RequestException as e:
        return f"Error de conexión con la API: {e}"

    except KeyError:
        return "Error: la respuesta de la API no tiene el formato esperado."


def construir_historial_conversacion(conversacion, limite=10):
    """
    Construye el historial de una conversación para enviarlo a la API.

    Importante:
    - No usa role='system' porque este modelo no lo soporta.
    - Evita roles repetidos seguidos, porque la API exige alternancia user/assistant.
    - Añade la instrucción inicial dentro del primer mensaje de usuario real.
    - Limita el historial a los últimos mensajes para no enviar conversaciones enormes.
    """

    mensajes = list(conversacion.mensajes.order_by('-id')[:limite])
    mensajes.reverse()

    instruccion = (
        "Responde como ChatIA, un asistente claro, útil y educativo. "
        "Ten en cuenta el historial de la conversación.\n\n"
    )

    historial = []

    for mensaje in mensajes:
        if mensaje.rol not in ["user", "assistant"]:
            continue

        contenido = mensaje.contenido

        if not historial and mensaje.rol == "user":
            contenido = instruccion + contenido

        if historial and historial[-1]["role"] == mensaje.rol:
            historial[-1]["content"] += "\n\n" + contenido
        else:
            historial.append({
                "role": mensaje.rol,
                "content": contenido
            })

    if not historial:
        historial.append({
            "role": "user",
            "content": instruccion + "Hola."
        })

    return historial


def crear_titulo_conversacion(prompt_usuario, modelo="google/gemma-2-2b-it", temperatura=0.7):
    """
    Genera un título corto para una conversación a partir del primer prompt.
    """
    api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        return "Nueva conversación"

    url = "https://integrate.api.nvidia.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    prompt_titulo = (
        f"Dime un título corto para el siguiente mensaje. "
        f"Devuelve solo el título, máximo 3 palabras: '{prompt_usuario[:100]}'"
    )

    payload = {
        "model": modelo,
        "messages": [
            {"role": "user", "content": prompt_titulo}
        ],
        "temperature": float(temperatura),
        "top_p": 0.7,
        "max_tokens": 10,
        "stream": False,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)

        if response.status_code != 200:
            return "Nueva conversación"

        data = response.json()
        titulo = data["choices"][0]["message"]["content"].strip()

        return titulo[:50] if titulo else "Nueva conversación"

    except Exception:
        return "Nueva conversación"


def convertir_markdown_a_html(texto):
    """
    Convierte texto Markdown en HTML para mostrarlo en la plantilla.
    No guarda HTML en la base de datos.
    """
    if not texto:
        return ""

    texto_seguro = escape(texto)

    html = markdown.markdown(
        texto_seguro,
        extensions=[
            "nl2br",
            "fenced_code",
            "tables",
        ]
    )

    return html


def preparar_mensajes_para_html(mensajes):
    """
    Añade a cada mensaje de la IA una versión HTML temporal para mostrar Markdown.
    No modifica la base de datos.
    """
    for mensaje in mensajes:
        if mensaje.rol == 'assistant':
            mensaje.respuesta_html = convertir_markdown_a_html(mensaje.contenido)
        else:
            mensaje.respuesta_html = mensaje.contenido

    return mensajes