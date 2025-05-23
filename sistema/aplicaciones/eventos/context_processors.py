from datetime import timedelta
from django.utils import timezone
from .models import Evento, Notificacion

def notificaciones_eventos_context_processor(request):
    if request.user.is_authenticated:
        ahora = timezone.now()
        proximos = Evento.objects.filter(
            usuario=request.user,
            fecha_evento__gte=ahora,
            fecha_evento__lte=ahora + timedelta(hours=24)
        )
        for e in proximos:
            # Verificamos si ya existe una notificación para este evento
            existe = Notificacion.objects.filter(evento=e, usuario=request.user).exists()
            if not existe:
                Notificacion.objects.create(
                    usuario=request.user,
                    evento=e,
                    mensaje=f"El evento '{e.titulo}' es en menos de 24 horas."
                )
                print(f"Notificación creada para: {e.titulo}")
        # Usamos el related_name "notificaciones_eventos" para obtener solo las notificaciones de eventos
        notis_no_leidas = request.user.notificaciones_eventos.filter(leida=False)
    else:
        notis_no_leidas = []
    return {'notificaciones_no_leidas': notis_no_leidas}

def notificaciones_unificadas_context_processor(request):
    if request.user.is_authenticated:
        total_eventos = request.user.notificaciones_eventos.filter(leida=False).count()
        total_control = request.user.notificaciones_control.filter(leida=False).count()
        total_no_leidas = total_eventos + total_control
    else:
        total_no_leidas = 0
    return {'total_no_leidas': total_no_leidas}
