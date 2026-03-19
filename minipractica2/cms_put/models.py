from django.db import models

# Create your models here.
class Contenido(models.Model):
    clave = models.CharField(max_length=64)
    valor = models.TextField()