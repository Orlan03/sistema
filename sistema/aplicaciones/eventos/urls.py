from django.urls import path
from .views import crear_evento, listar_eventos, editar_evento, eliminar_evento, todas_notificaciones, notificaciones_unificadas

app_name = 'eventos'

urlpatterns = [
    path('crear/', crear_evento, name='crear_evento'),
    path('listar/', listar_eventos, name='listar_eventos'),
    path('editar/<int:evento_id>/', editar_evento, name='editar_evento'),
    path('eliminar/<int:evento_id>/', eliminar_evento, name='eliminar_evento'),
    path('notificaciones/', todas_notificaciones, name='todas_notificaciones'),
    path('', notificaciones_unificadas, name='unificadas'),
    path('notificaciones/unificadas/', notificaciones_unificadas, name='unificadas'),
]
