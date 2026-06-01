from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    # publicas
    path('', views.home, name='home'),
    path('ayuda/', views.ayuda, name='ayuda'),

    # gestion de usuarios
    path('registro/', views.registro, name='registro'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='cuenta'), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # gestion de cuentas una vez registrado
    path('cuenta/', views.cuenta, name='cuenta'),
    path('cuenta/<str:nombre>/configuracion/', views.configuracion_cuenta, name='configuracion'),

    #gestion de conversaciones una vez registrado
    path('crear_conversacion/', views.crear_conversacion, name='crear_conversacion'),
    path('iniciar_conversacion/', views.iniciar_conversacion, name='iniciar_conversacion'),
    path('actualizar_mensajes/<int:conv_id>/', views.actualizar_mensajes, name='actualizar_mensajes'),
    path('borrar_conversacion/<int:conv_id>/', views.borrar_conversacion, name='borrar_conversacion'),

    # generar json de una conversación específica con un id
    path('cuenta/conversacion/<int:conv_id>/json/', views.conversacion_json, name='conversacion_json'),
]

handler404 = "chatbot.views.error_404" # gestión de errores de páginas no declaradas (404)