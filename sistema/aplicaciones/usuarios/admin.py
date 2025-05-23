from django.contrib import admin
from .models import Empleado

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'celular')  # Campos que se verán en la lista
    search_fields = ('nombres', 'apellidos', 'cedula')  # Campos por los cuales se puede buscar
    list_filter = ('cedula', 'celular')  # Opciones de filtro en el panel de administración
    ordering = ('nombres',)  # Orden por defecto
    list_per_page = 10  # Número de elementos por página

# Registrar el modelo Empleado en el admin
admin.site.register(Empleado, EmpleadoAdmin)
