from django.urls import path
from .views import *
app_name = 'control_procesos'

urlpatterns = [
    
    path('listar/<int:carpeta_id>/', listar_procesos, name='listar_procesos'),
    path('registrar/<int:carpeta_id>/', registrar_proceso, name='registrar_proceso'),
    path('', listar_carpetas, name='listar_carpetas'),
    path("editar/<int:proceso_id>/", editar_proceso, name="editar_proceso"),
    path("eliminar/<int:proceso_id>/", eliminar_proceso, name="eliminar_proceso"),
    path('respuestas/registrar/<int:carpeta_id>/', registrar_respuesta, name='registrar_respuesta'),
    path('respuestas/', listar_respuestas, name='listar_respuestas'),
    path('respuestas/subcarpeta/<int:carpeta_id>/', listar_respuestas_subcarpeta, name='listar_respuestas_subcarpeta'),
    path('respuestas/por_nombre/<int:carpeta_id>/', listar_respuestas_por_nombre, name='listar_respuestas_por_nombre'),
    path('respuestas/editar/<int:respuesta_id>/', editar_respuesta, name='editar_respuesta'),
    path('eliminar/<int:respuesta_id>/', eliminar_respuesta, name='eliminar_respuesta'),
    path("cuentas/listar/<int:carpeta_id>/", listar_cuentas_por_cobrar, name="listar_cuentas_por_cobrar"),
    path('cuentas/registrar/<int:carpeta_id>/', registrar_cuenta_por_cobrar, name='registrar_cuenta_por_cobrar'),
    path('cuentas/editar/<int:cuenta_id>/', editar_cuenta_por_cobrar, name='editar_cuenta_por_cobrar'),
    path('cuentas/eliminar/<int:cuenta_id>/', eliminar_cuenta_por_cobrar, name='eliminar_cuenta_por_cobrar'),
    path('cxc/crear/<int:carpeta_id>/', crear_cxc_tacae, name='crear_cxc'),
    path('cxc/editar/<int:cxc_id>/', editar_cxc, name='editar_cxc'),
    path('cxc/eliminar/<int:cxc_id>/', eliminar_cxc, name='eliminar_cxc'),
    path('firmas/crear/<int:carpeta_id>/', crear_firma, name='crear_firma'),
    path('firmas/editar/<int:firma_id>/',editar_firma, name='editar_firma'),
    path('firmas/eliminar/<int:firma_id>/',eliminar_firma, name='eliminar_firma'),
    path('cuentas_especiales/crear/<int:carpeta_id>/', crear_cuenta_especial, name='crear_cuenta_especial'),
    path('cuentas_especiales/editar/<int:cuenta_id>/', editar_cuenta_especial, name='editar_cuenta_especial'),
    path('cuentas_especiales/eliminar/<int:cuenta_id>/', eliminar_cuenta_especial, name='eliminar_cuenta_especial'),
    path('preguntas/crear/<int:carpeta_id>/', crear_pregunta, name='crear_pregunta'),
    path('preguntas/editar/<int:pregunta_id>/', editar_pregunta, name='editar_pregunta'),
    path('preguntas/eliminar/<int:pregunta_id>/', eliminar_pregunta, name='eliminar_pregunta'),
    path('claves_sistemas/crear/<int:carpeta_id>/', crear_claves_sistemas, name='crear_claves_sistemas'),
    path('claves_sistemas/editar/<int:claves_id>/', editar_claves_sistemas, name='editar_claves_sistemas'),
    path('claves_sistemas/eliminar/<int:claves_id>/', eliminar_claves_sistemas, name='eliminar_claves_sistemas'),
    path('sistemas/crear/<int:carpeta_id>/', crear_sistema, name='crear_sistema'),
    path('sistemas/editar/<int:sistema_id>/', editar_sistema, name='editar_sistema'),
    path('sistemas/eliminar/<int:sistema_id>/', eliminar_sistema, name='eliminar_sistema'),
    path('banco/crear/<int:carpeta_id>/', crear_banco, name='crear_banco'),
    path('banco/editar/<int:banco_id>/', editar_banco, name='editar_banco'),
    path('banco/eliminar/<int:banco_id>/', eliminar_banco, name='eliminar_banco'),
    
    path('noti/ver/<int:noti_id>/',marcar_y_ver_carpeta,name='marcar_y_ver_carpeta'),

    
]
    
