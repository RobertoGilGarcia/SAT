

# ENTREGA CONVOCATORIA MAYO

# ENTREGA DE PRÁCTICA

## Datos

* Nombre: Roberto Gil García
* Titulación: Ingeniería en Tecnologías de la Telecomunicación
* Cuenta en laboratorios: roberto
* Cuenta URJC: r.gil.2022@alumnos.urjc.es
* Video básico (url): https://youtu.be/OwczVRX9irI
* Video parte opcional (url): https://youtu.be/92bj4jE-YUc
* Despliegue (url): https://robertourjc.pythonanywhere.com/
* Contraseñas: 
    * roberto / gilgarcia
    * victor / tejedorsacristan
    * daniel / hernangomez
    * david / bisbalferre

## Recursos implementados y métodos disponibles para cada recurso

* Recurso: `/admin/`
  * Métodos permitidos: GET, POST
  * Descripción: Admin site de Django



* Recurso: `/`
  * Métodos permitidos: GET, POST
  * Descripción: Página principal de ChatIA y prueba gratuita de la IA


* Recurso : `/ayuda/`
  * Métodos permitidos: GET
  * Descripción: Página de ayuda de ChatIA pública


* Recurso : `/registro/`
  * Métodos permitidos: GET, POST
  * Descripción: Página para poder registrarte y tener gestión de conversaciones en ChatIA


* Recurso : `/login`
  * Métodos permitidos: GET, POST
  * Descripción: Página para poder iniciar sesión en tu cuenta y modificar, consultar o crear conversaciones con la IA


* Recurso : `/cuenta`
  * Métodos permitidos: GET
  * Descripción: Página para mostrar la interfaz de la cuenta una vez te has registrado y logueado


* Recurso : `/cuenta/<str:nombre>/configuracion/`
  * Métodos permitidos: GET, POST
  * Descripción: Página para mostrar la interfaz de la configuración de la cuenta una vez te has registrado y logueado


* Recurso : `/crear_conversacion/`
  * Métodos permitidos: POST
  * Descripción: Botón para crear una nueva conversación dentro de tu cuenta


* Recurso : `/iniciar_conversacion/`
  * Métodos permitidos: POST
  * Descripción: Crea una conversación únicamente con el primer prompt enviado a la IA


* Recurso : `/actualizar_mensajes/<int:conv_id>/`
  * Métodos permitidos: POST
  * Descripción: Añade tanto el prompt del usuario como la respuesta de la IA a la conversación


* Recurso : `/borrar_conversacion/<int:id_conv>`
  * Métodos permitidos: POST
  * Descripción: Botón para borrar una conversación con un id específico dentro de tu cuenta


* Recurso: `/cuenta/conversacion/<int:conv_id>/json/`
  * Métodos permitidos: GET
  * Descripción: Botón para mostrar el objeto de la conversación en una página nueva

## Resumen parte obligatoria

ChatIA es una aplicación en Django que permite a los usuarios registrarse, iniciar sesión, cerrar sesión y gestionar los chats con la IA.

El proyecto incluye una página principal pública, una página de ayuda, sistema de registro/login/logout, configuración de usuario con alias, email y tema visual, y una estructura común con cabecera, menú y footer en todas las páginas. El footer muestra métricas como conversaciones totales, mensajes totales, conversaciones del usuario y prompts del usuario.

La interfaz utiliza plantillas, CSS y Bootstrap para los estilos. Además, incorpora HTMX para actualizar dinámicamente el chat, la lista de conversaciones y el footer sin recargar toda la página.

También se ofrece un recurso JSON que exporta una conversación completa con sus datos y mensajes. Este recurso está protegido para que cada usuario solo pueda acceder a sus propias conversaciones.

La aplicación se conecta a NVIDIA Build mediante un API token para generar respuestas reales de la IA. El API KEY se gestiona mediante variable de entorno

Además, se han añadido tests básicos extremo a extremo para comprobar recursos principales y un test unitario sencillo. También se registra la base de datos en el Admin Site para poder gestionar los modelos desde la interfaz de administración.

## Lista partes opcionales

* Prueba de la IA "gratuita" : esta funcionalidad se ha incorporado a modo de prueba de la web, lo que se pregunta a la IA en esta implementación, no se guarda en la base de datos


* Inclusión del favicon : el favicon se gestiona en los ficheros estáticos del proyecto


* Selección del tema visual : en la configuración de la cuenta puedes elegir entre tema claro u oscuro dependiendo de tus preferecias, si no estás registrado o quieres el predeterminado, es el tema claro.


* Inclusión de HTMX en elementos adicionales : HTMX está presente tanto en los mensajes con la IA, como en las métricas en el footer, como en el nombre de la conversación.


* Inclusión de HTMX en respuestas de la IA: Cuando estas registrado y envías un prompt, sale un indicador de HTMX mientras la IA está "pensando" en tu respuesta.


* Soporte multi-chat avanzado : posibilidad de borrar conversaciones en tu cuenta.


* Respuestas de la IA con decoración en Markdown: Ya que las respuestas de la IA responden en formato Markdown, se ha aprovechado para implementar la traducción de "texto Markdown" a HTML para poder imprimir las respuestas con las normas de Markdown.
