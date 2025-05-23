from django import forms
from .models import Carpeta, Documento



class CarpetaForm(forms.ModelForm):
    class Meta:
        model = Carpeta
        fields = ['nombre']  # Solo permitir ingresar el nombre de la carpeta
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la carpeta'})
        }




class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre', 'archivo']
