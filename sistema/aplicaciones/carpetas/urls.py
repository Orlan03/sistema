from django.urls import path
from . import views

app_name = 'carpetas'  # Asegurar el namespace

urlpatterns = [
    path('', views.listar_carpetas, name='listar_carpetas'),
    path('crear/', views.crear_carpeta, name='crear_carpeta'),
    path('ver/<int:carpeta_id>/', views.ver_carpeta, name='ver_carpeta'),
    path('eliminar/<int:carpeta_id>/', views.eliminar_carpeta, name='eliminar_carpeta'),
    path('subir/<int:carpeta_id>/', views.subir_documento, name='subir_documento'),  
    path('crear-subcarpeta/<int:carpeta_id>/', views.crear_subcarpeta, name='crear_subcarpeta'),
]
