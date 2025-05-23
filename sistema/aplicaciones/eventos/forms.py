# aplicaciones/eventos/forms.py
from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'fecha_evento', 'descripcion']
        widgets = {
            'fecha_evento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
