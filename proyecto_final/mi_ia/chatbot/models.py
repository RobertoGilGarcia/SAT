from django.db import models

# Create your models here.
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE) #OneToOneField es debido a que un perfil solo pertenece a un usuario, la relacion tiene que ser 1 - 1
    alias = models.CharField(max_length=50)
    foto_perfil = models.ImageField(upload_to='fotos_perfil', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.alias