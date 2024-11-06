from django import forms

from .models import UrlRedirect


class UrlRedirectForm(forms.ModelForm):
    class Meta:
        model = UrlRedirect
        fields = ['destino', 'slug']
        widgets = {
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cole seu link aqui...'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escolha seu slug (opcional)'}),
        }
