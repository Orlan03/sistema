from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="eventos")
    titulo = models.CharField(max_length=200)
    fecha_evento = models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)  # Agrega este campo

    def __str__(self):
        return self.titulo

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificaciones_eventos")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensaje
