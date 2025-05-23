# aplicaciones/notificaciones_context_processor.py (o en una app que prefieras)
def notificaciones_unificadas_context_processor(request):
    if request.user.is_authenticated:
        total_eventos = request.user.notificaciones_eventos.filter(leida=False).count()
        total_control = request.user.notificaciones_control.filter(leida=False).count()
        total_no_leidas = total_eventos + total_control
    else:
        total_no_leidas = 0
    return {
        'total_no_leidas': total_no_leidas
    }
