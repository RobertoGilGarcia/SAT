from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(
        label='Pregúntale algo a la IA',
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Escribe aquí tu pregunta...'
        })
    )

