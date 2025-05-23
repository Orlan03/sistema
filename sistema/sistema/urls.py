from django.contrib import admin
from django.urls import path, include
from aplicaciones.usuarios import views as usuarios_views
from aplicaciones.carpetas import views as carpeta_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usuarios_views.login_view, name='login'),  # Vista para login
    path('inicio/', usuarios_views.home_view, name='home'),  # Vista para home
    path('', include('aplicaciones.usuarios.urls')),
    path('documentos/', include(('aplicaciones.carpetas.urls', 'carpetas'), namespace='carpetas')),
    path('eventos/', include(('aplicaciones.eventos.urls', 'eventos'), namespace='eventos')),
    path('procesos/', include(('aplicaciones.control_procesos.urls', 'procesos'), namespace='procesos')),
    path('notificaciones/', include(('aplicaciones.eventos.urls', 'eventos'), namespace='notificaciones')),


   
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)