from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from .models import Empleado


class UsernameOrCedulaBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Primero intenta buscar por username
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

        # Luego intenta buscar por cedula en el modelo Empleado
        try:
            empleado = Empleado.objects.get(cedula=username)
            user = empleado.usuario
            if user.check_password(password):
                return user
        except Empleado.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
