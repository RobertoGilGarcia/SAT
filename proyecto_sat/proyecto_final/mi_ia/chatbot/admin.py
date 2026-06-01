from django.contrib import admin

# Register your models here.
from .models import PerfilUsuario, Conversacion, Mensaje


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'alias', 'tema', 'fecha_creacion')
    search_fields = ('usuario__username', 'alias')
    list_filter = ('tema', 'fecha_creacion')


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('titulo', 'usuario__username')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_actualizacion',)


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('conversacion', 'rol', 'fecha_creacion')
    search_fields = ('contenido', 'conversacion__titulo', 'conversacion__usuario__username')
    list_filter = ('rol', 'fecha_creacion')
    ordering = ('-fecha_creacion',)