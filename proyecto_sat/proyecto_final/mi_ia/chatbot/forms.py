from django import forms
from .models import PerfilUsuario

class PromptForm(forms.Form):
    prompt = forms.CharField(label='Pregúntale algo a la IA',widget=forms.Textarea(attrs={'rows': 1,'class': 'form-control chat-textarea','placeholder': 'Escribe aquí tu pregunta...'}))


class PerfilUsuarioForm(forms.ModelForm): # email manual porque está en users de django
    email = forms.EmailField(required=False,label='Correo electrónico',widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Introduce tu correo electrónico'}))

    class Meta: # meta porque tiene que heredar de PerfilUsuario para añadirle más campos
        model = PerfilUsuario
        fields = ['alias','tema',]

        widgets = {'alias': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Introduce un alias para mostrar en ChatIA'}),
                   'tema': forms.Select(attrs={'class': 'form-select'}),}

        labels = {'alias': 'Alias visible',
                  'tema': 'Tema visual',}