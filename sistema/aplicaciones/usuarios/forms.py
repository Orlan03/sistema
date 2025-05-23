from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Empleado

class EmpleadoForm(forms.ModelForm):
    # Campos para la contraseña (opcionales en edición)
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Contraseña", 
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Confirmar Contraseña", 
        required=False
    )
    # Campo para el nombre de usuario (del objeto User)
    username = forms.CharField(
        max_length=150, 
        label="Nombre de usuario", 
        required=False
    )

    class Meta:
        model = Empleado
        fields = ['nombres', 'apellidos', 'cedula', 'celular']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando un empleado existente, pre-llenar el campo username
        if self.instance and self.instance.pk:
            if self.instance.usuario:
                self.fields['username'].initial = self.instance.usuario.username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if (password or confirm_password) and password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


class UsernameOrCedulaAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario o cédula", 
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Ingrese su usuario o cédula'}),
        error_messages={'required': 'Por favor, ingrese su usuario o cédula.'}
    )
