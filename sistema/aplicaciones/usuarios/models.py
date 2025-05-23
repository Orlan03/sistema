# models.py
from django.db import models
from django.contrib.auth.models import User

class Empleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    cedula = models.CharField(max_length=10, unique=True)
    celular = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
