from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import PerfilUsuario, Conversacion, Mensaje


class Tests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="roberto",
            password="12345"
        )

        PerfilUsuario.objects.create(
            usuario=self.usuario,
            alias="RobertoIA",
            tema="claro"
        )

        self.conversacion = Conversacion.objects.create(
            usuario=self.usuario,
            titulo="Conversación de prueba"
        )

        Mensaje.objects.create(
            conversacion=self.conversacion,
            rol="user",
            contenido="Hola"
        )

        Mensaje.objects.create(
            conversacion=self.conversacion,
            rol="assistant",
            contenido="Hola, soy ChatIA"
        )

    def test_home_funciona(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ChatIA")

    def test_cuenta_sin_login_redirige(self):
        response = self.client.get(reverse("cuenta"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_cuenta_con_login_funciona(self):
        self.client.login(username="roberto", password="12345")
        response = self.client.get(reverse("cuenta"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Conversación de prueba")

    def test_recurso_json_funciona(self):
        self.client.login(username="roberto", password="12345")

        response = self.client.get(
            reverse("conversacion_json", args=[self.conversacion.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        datos = response.json()
        self.assertEqual(datos["titulo"], "Conversación de prueba")
        self.assertEqual(datos["usuario"], "roberto")
        self.assertEqual(datos["total_mensajes"], 2)


    def test_unitario_str_perfil_usuario(self):
        perfil = PerfilUsuario.objects.get(usuario=self.usuario)
        self.assertEqual(str(perfil), "RobertoIA")