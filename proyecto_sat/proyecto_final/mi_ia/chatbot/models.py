from django.db import models

# Create your models here.
class PerfilUsuario(models.Model): # hereda de User de django porque es más seguro, pero le añade campos
    usuario = models.OneToOneField('auth.User',on_delete=models.CASCADE,related_name='perfil')
    alias = models.CharField(max_length=50, blank=True)
    tema = models.CharField(max_length=20,choices=[('claro', 'Claro'),('oscuro', 'Oscuro'),],default='claro')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.alias:
            return self.alias
        return f"Perfil de {self.usuario.username}"

class Conversacion(models.Model): #es una ForeignKey de User, porque cada usuario puede tener varias conversaciones
    usuario = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name='conversaciones')
    titulo = models.CharField(max_length=100, default='Nueva conversación')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.usuario.username})"


class Mensaje(models.Model): # es una ForignKey de Conversacion, porque cada conversación tiene varios mensajes
    conversacion = models.ForeignKey(Conversacion,on_delete=models.CASCADE,related_name='mensajes')
    rol = models.CharField(max_length=10,choices=[('user','Usuario'),('assistant','ChatIA')])
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rol}: {self.contenido[:50]}"