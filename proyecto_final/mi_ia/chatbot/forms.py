from django import forms
from .models import PerfilUsuario


class PromptForm(forms.Form):
    prompt = forms.CharField(
        label='Pregúntale algo a la IA',
        widget=forms.Textarea(attrs={
            'rows': 1,
            'class': 'form-control chat-textarea',
            'placeholder': 'Escribe aquí tu pregunta...'
        })
    )


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['alias', 'foto_perfil']

        widgets = {
            'alias': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu alias'
            }),
        }