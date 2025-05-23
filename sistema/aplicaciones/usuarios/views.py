from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import EmpleadoForm, UsernameOrCedulaAuthenticationForm
from .models import Empleado
from django.contrib.auth.models import User

# Vista de inicio de sesión
def login_view(request):
    if request.method == "POST":
        form = UsernameOrCedulaAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Se autenticará mediante el backend personalizado
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas.')
    else:
        form = UsernameOrCedulaAuthenticationForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

# Vista del Home (definida una sola vez)
@login_required
def home_view(request):
    return render(request, 'usuarios/home.html', {'usuario': request.user.username})

# Función para verificar si el usuario es dueño (admin)
def is_owner(user):
    return user.is_authenticated and user.is_staff

# Registrar Empleado (solo el dueño puede hacerlo)
@user_passes_test(is_owner)
@login_required
def registrar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Verifica que el usuario no exista
            if User.objects.filter(username=username).exists():
                messages.error(request, "El nombre de usuario ya está en uso.")
                return render(request, 'usuarios/registrar_empleado.html', {'form': form})
            
            # Crear el usuario
            user = User.objects.create_user(username=username, password=password)
            
            # Asignar el usuario al modelo Empleado
            empleado = form.save(commit=False)
            empleado.usuario = user
            empleado.save()
            
            messages.success(request, "Empleado registrado con éxito.")
            return redirect('home')
    else:
        form = EmpleadoForm()
    
    return render(request, 'usuarios/registrar_empleado.html', {'form': form})

# Vista para listar empleados
@user_passes_test(is_owner)
@login_required
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'usuarios/lista_empleados.html', {'empleados': empleados})

# Editar empleado
@user_passes_test(is_owner)
@user_passes_test(is_owner)
def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    usuario_asociado = empleado.usuario  # Obtén el usuario relacionado

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado_obj = form.save(commit=False)
            # Actualizar nombre de usuario si cambió
            nuevo_username = form.cleaned_data.get('username')
            if nuevo_username and nuevo_username != usuario_asociado.username:
                # Verificar que no exista otro user con ese username
                if User.objects.filter(username=nuevo_username).exclude(pk=usuario_asociado.pk).exists():
                    form.add_error('username', 'Ese nombre de usuario ya está en uso.')
                    return render(request, 'usuarios/editar_empleado.html', {'form': form})
                usuario_asociado.username = nuevo_username

            # Actualizar la contraseña si se ingresa una nueva
            new_password = form.cleaned_data.get('password')
            if new_password:
                usuario_asociado.set_password(new_password)

            usuario_asociado.save()  # Guarda cambios en el objeto User

            # Aseguramos que el empleado mantenga la relación con el mismo usuario
            empleado_obj.usuario = usuario_asociado
            empleado_obj.save()

            messages.success(request, "Empleado actualizado exitosamente.")
            # Redirige a la misma vista para que se muestre el mensaje
            return redirect('editar_empleado', pk=empleado.pk)
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'usuarios/editar_empleado.html', {'form': form})

# Eliminar empleado
@user_passes_test(is_owner)
@login_required
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    empleado.delete()
    messages.success(request, 'Empleado eliminado exitosamente.')
    return redirect('lista_empleados')

# Dashboard del jefe
@user_passes_test(is_owner)
@login_required
def jefe_dashboard(request):
    return render(request, 'usuarios/jefe_dashboard.html')

# Ejemplo de un backend (aunque aquí tienes dos aproximaciones: CedulaBackend y UsernameOrCedulaBackend)
class CedulaBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        En este backend, el campo 'username' contendrá la cédula.
        Buscamos el Empleado correspondiente y obtenemos su usuario asociado.
        """
        try:
            empleado = Empleado.objects.get(cedula=username)
            user = empleado.usuario
        except Empleado.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
