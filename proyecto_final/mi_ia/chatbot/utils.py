import os
import requests

def llamar_ia_nvidia(prompt_usuario):
    """
    Envía el prompt del usuario a la API de NVIDIA Build
    y devuelve la respuesta generada por el modelo.
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
        "messages": [
            {
                "role": "user",
                "content": prompt_usuario
            }
        ],
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