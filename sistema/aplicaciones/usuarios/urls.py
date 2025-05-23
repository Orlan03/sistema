from django.urls import path
from . import views
from .views import *



urlpatterns = [
    path('login/', views.login_view, name='login'),  # Ruta para login
    path('inicio/', views.home_view, name='home'),  # Ruta para la página de inicio después de login
    path('empleado/registrar/', views.registrar_empleado, name='registrar_empleado'),  # Registrar empleado
    path('empleados/', lista_empleados, name='lista_empleados'),
    path('empleados/registrar/', registrar_empleado, name='registrar_empleado'),
    path('empleados/editar/<int:pk>/', editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:pk>/', eliminar_empleado, name='eliminar_empleado'),
]
