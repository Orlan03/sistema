from django.db import models

from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Carpeta(models.Model):
    nombre = models.CharField(max_length=200)
    padre = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='subcarpetas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre



class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name='documentos')
    
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre