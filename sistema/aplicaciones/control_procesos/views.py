from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from aplicaciones.carpetas.models import Carpeta
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.urls import reverse  
from django.contrib.auth.models import User

from aplicaciones.usuarios.models import Empleado
def obtener_todas_subcarpetas(carpeta, visitadas=None):
    """Recupera todas las subcarpetas dentro de una carpeta, sin importar el nivel"""
    if visitadas is None:
        visitadas = set()
    
    subcarpetas = list(Carpeta.objects.filter(padre=carpeta))
    for sub in subcarpetas:
        if sub.id not in visitadas:  # Evita ciclos infinitos
            visitadas.add(sub.id)
            subcarpetas.extend(obtener_todas_subcarpetas(sub, visitadas))
    return subcarpetas

@login_required
def registrar_proceso(request, carpeta_id):
    """Registra un nuevo proceso y crea una carpeta con el mismo nombre dentro de la carpeta seleccionada,
    pero el proceso se guarda en la carpeta donde se hizo clic en 'Registrar Nuevo Proceso'."""

    carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)  # Carpeta donde se hizo clic (ejemplo: "Gualaceo")

    if request.method == "POST":
        form = ProcesoForm(request.POST)
        if form.is_valid():
            proceso = form.save(commit=False)

            # Validar si "carpeta_id" viene en la solicitud POST
            carpeta_destino_id = request.POST.get("carpeta_id")
            if not carpeta_destino_id:
                return render(request, "control_procesos/registrar_proceso.html", {
                    "form": form,
                    "subcarpetas": Carpeta.objects.filter(padre=carpeta_padre),
                    "carpeta_padre": carpeta_padre,
                    "error": "⚠ Debes seleccionar una subcarpeta para guardar el proceso.",
                })

            carpeta_destino = get_object_or_404(Carpeta, id=carpeta_destino_id)

            # Crear la carpeta con el nombre del proceso dentro de la carpeta seleccionada
            nueva_carpeta, created = Carpeta.objects.get_or_create(nombre=proceso.proceso, padre=carpeta_destino)

            # Guardar el proceso en la carpeta donde se hizo clic en "Registrar Nuevo Proceso"
            proceso.carpeta = carpeta_padre
            proceso.save()

            return redirect("carpetas:ver_carpeta", carpeta_id=carpeta_padre.id)

    else:
        form = ProcesoForm()

    # Obtener o crear la carpeta "Informes Periciales Grupo TACAE"
    informes_periciales, _ = Carpeta.objects.get_or_create(nombre="Informes Periciales Grupo TACAE", padre=None)
    subcarpetas = Carpeta.objects.filter(padre=informes_periciales)

    return render(request, "control_procesos/registrar_proceso.html", {
        "form": form,
        "subcarpetas": subcarpetas,
        "carpeta_padre": carpeta_padre,
    })

@login_required
def listar_procesos(request, carpeta_id):
    """Lista solo los procesos de la carpeta seleccionada."""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    procesos = Proceso.objects.filter(carpeta=carpeta)

    return render(request, 'control_procesos/listar_procesos.html', {
        'procesos': procesos,
        'carpeta': carpeta
    })

@login_required
def listar_carpetas(request):
    informes_periciales, _ = Carpeta.objects.get_or_create(nombre="Informes Periciales Grupo TACAE", padre=None)
    carpetas = Carpeta.objects.filter(padre=None)
    return render(request, 'carpetas/listar_carpetas.html', {'carpetas': carpetas})

@login_required
def ver_proceso(request, proceso_id):
    """
    Muestra los detalles de un proceso específico.
    """
    proceso = get_object_or_404(Proceso, id=proceso_id)
    return render(request, 'control_procesos/ver_proceso.html', {'proceso': proceso})

@login_required
def eliminar_proceso(request, proceso_id):
    """
    Elimina un proceso y redirige a la carpeta donde estaba almacenado.
    """
    proceso = get_object_or_404(Proceso, id=proceso_id)
    carpeta_id = proceso.carpeta.id  # Obtener la carpeta donde estaba el proceso
    proceso.delete()
    messages.success(request, "Proceso eliminado correctamente.")
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)

@login_required
def editar_proceso(request, proceso_id):
    """Permite editar un proceso existente."""
    proceso = get_object_or_404(Proceso, id=proceso_id)

    if request.method == "POST":
        form = ProcesoForm(request.POST, instance=proceso)
        if form.is_valid():
            form.save()
            return redirect("carpetas:ver_carpeta", carpeta_id=proceso.carpeta.id)  # Redirigir a la carpeta donde está el proceso
    else:
        form = ProcesoForm(instance=proceso)

    return render(request, "control_procesos/editar_proceso.html", {"form": form, "proceso": proceso})


##############################Respuestas#####################################3

@login_required
def registrar_respuesta(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)

    if request.method == "POST":
        form = RespuestaForm(request.POST)
        if form.is_valid():
            # 1) Creamos la Respuesta sin guardarla aún
            nueva_respuesta = form.save(commit=False)
            nueva_respuesta.carpeta = carpeta

            # 2) Creamos un Proceso nuevo con el nombre que ingresó el usuario
            nombre = form.cleaned_data['nombre_proceso']
            proceso = Proceso.objects.create(
                proceso=nombre,
                carpeta=carpeta,
                # Rellena aquí los demás campos obligatorios de Proceso...
            )
            nueva_respuesta.proceso = proceso

            # 3) Guardamos la Respuesta ya vinculada
            nueva_respuesta.save()

            messages.success(request, "✅ Respuesta registrada correctamente.")
            return redirect("carpetas:ver_carpeta", carpeta_id=carpeta.id)
    else:
        form = RespuestaForm()

    # Ya no necesitas pasar carpetas_con_procesos al template
    return render(request, "control_procesos/registrar_respuesta.html", {
        "form": form,
        "carpeta": carpeta,
    })
@login_required
def listar_respuestas_subcarpeta(request, carpeta_id):
    """Lista las respuestas de una subcarpeta en 'Respuestas'."""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    
    # 🔥 IMPORTANTE: Filtrar solo respuestas que pertenecen a esta carpeta
    respuestas = Respuesta.objects.filter(carpeta=carpeta)

    return render(request, "control_procesos/listar_respuesta.html", {
        "carpeta": carpeta,
        "respuestas": respuestas
    })
    

@login_required
def listar_respuestas_por_nombre(request, carpeta_id):
    # Esta carpeta es la de la sección de Respuestas (por ejemplo, "Cuenca")
    carpeta_respuesta = get_object_or_404(Carpeta, id=carpeta_id)
    # Filtra las respuestas de los procesos que estén en una carpeta con el mismo nombre
    # y que pertenezcan a "Procesos Pendientes"
    respuestas = Respuesta.objects.filter(
        proceso__carpeta__nombre=carpeta_respuesta.nombre,
        proceso__carpeta__padre__nombre="Procesos Pendientes"
    )
    return render(request, 'control_procesos/listar_respuestas_subcarpeta.html', {
        'carpeta': carpeta_respuesta,
        'respuestas': respuestas,
    })

@login_required
def listar_respuestas(request):
    respuestas = Respuesta.objects.all()  # Ajusta según tus necesidades
    return render(request, 'control_procesos/listar_respuestas.html', {'respuestas': respuestas})

@login_required

@login_required
def editar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id=respuesta_id)
    if request.method == "POST":
        form = RespuestaForm(request.POST, instance=respuesta)
        if form.is_valid():
            # Guardar sin commit para modificar el objeto
            respuesta_instance = form.save(commit=False)
            # Si el campo fecha_respuesta está vacío, asignamos la fecha actual
            if not respuesta_instance.fecha_respuesta:
                respuesta_instance.fecha_respuesta = datetime.date.today()
            respuesta_instance.save()
            # Redirige a la carpeta asociada (ajusta según tu flujo)
            return redirect('carpetas:ver_carpeta', respuesta_instance.carpeta.id)
    else:
        form = RespuestaForm(instance=respuesta)
    return render(request, 'control_procesos/editar_respuesta.html', {'form': form, 'respuesta': respuesta})



@login_required
def eliminar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, id=respuesta_id)
    if request.method == "POST":
        respuesta.delete()
        # Redirige a la lista de respuestas o a la carpeta correspondiente
        return redirect('respuestas:listar_respuestas')
    return render(request, 'respuestas/eliminar_respuesta.html', {'respuesta': respuesta})
    
######################### CUENTAS POR COBRAR #############################




@login_required
def registrar_cuenta_por_cobrar(request, carpeta_id):
    """Registra un nuevo cobro, permitiendo seleccionar un proceso de forma organizada."""
    
    # Carpeta “padre” desde la URL
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)

    if request.method == "POST":
        form = CuentaPorCobrarForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.carpeta = carpeta
            cuenta.save()
            # Redirige correctamente a la vista de la carpeta padre
            return redirect("carpetas:ver_carpeta", carpeta.id)
    else:
        form = CuentaPorCobrarForm()

    # 🌟 Construyo el dict de carpetas → procesos sin pisar la variable 'carpeta'
    carpetas_con_procesos = {}
    for c in Carpeta.objects.all():
        procesos = Proceso.objects.filter(carpeta=c)
        if procesos.exists():
            carpetas_con_procesos[c] = procesos

    return render(request, "control_procesos/registrar_cuenta.html", {
        "form": form,
        "carpeta": carpeta,                     # sigue siendo la carpeta padre
        "carpetas_con_procesos": carpetas_con_procesos,
    })

    
def editar_cuenta_por_cobrar(request, cuenta_id):
    """
    Vista para editar un registro de CuentaPorCobrar existente.
    """
    cuenta = get_object_or_404(CuentaPorCobrar, id=cuenta_id)
    
    if request.method == 'POST':
        form = CuentaPorCobrarForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()  # Se recalculará 'saldo' en el método 'save()' del modelo
            return redirect('carpetas:ver_carpeta', carpeta_id=cuenta.carpeta.id)
    else:
        form = CuentaPorCobrarForm(instance=cuenta)
    
    return render(request, 'control_procesos/editar_cuenta.html', {
        'form': form,
        'cuenta': cuenta
    })
    
def eliminar_cuenta_por_cobrar(request, cuenta_id):
    cuenta = get_object_or_404(CuentaPorCobrar, id=cuenta_id)
    carpeta_id = cuenta.carpeta.id
    cuenta.delete()
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)




def listar_cuentas_por_cobrar(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)

    # Cuentas a mostrar (todas al inicio)
    cuentas = CuentaPorCobrar.objects.filter(carpeta=carpeta).select_related('proceso__responsable')

    # Filtro GET
    responsable_id = request.GET.get("responsable")
    if responsable_id:
        cuentas = cuentas.filter(proceso__responsable__id=responsable_id)

    # ✅ Lista completa de responsables de esta carpeta (no de las cuentas ya filtradas)
    responsables_ids = CuentaPorCobrar.objects.filter(
        carpeta=carpeta, proceso__responsable__isnull=False
    ).values_list("proceso__responsable__id", flat=True).distinct()

    responsables = User.objects.filter(id__in=responsables_ids)

    total_cobrado = sum(c.cobro or 0 for c in cuentas)
    total_saldo = sum(c.saldo or 0 for c in cuentas)

    return render(request, "control_procesos/listar_cuentas.html", {
        "carpeta": carpeta,
        "cuentas": cuentas,
        "responsables": responsables,
        "filtro_responsable": responsable_id,
        "total_cobrado": total_cobrado,
        "total_saldo": total_saldo,
    })


###############################CXC#########################
@login_required
def crear_cxc_tacae(request, carpeta_id):
    # Obtener la subcarpeta actual
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    
    if request.method == 'POST':
        form = CXCForm(request.POST)
        if form.is_valid():
            nueva_cxc = form.save(commit=False)
            nueva_cxc.carpeta = carpeta  # Se asocia a la subcarpeta
            nueva_cxc.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = CXCForm()
    
    return render(request, 'control_procesos/crear_cxc.html', {
        'form': form,
        'carpeta': carpeta
    })
@login_required
def editar_cxc(request, cxc_id):
    """
    Vista para editar (y actualizar) un registro de CXC.
    Se muestra el formulario con los datos actuales y, al enviarlo,
    se actualiza el registro.
    """
    cxc = get_object_or_404(CXC, id=cxc_id)
    if request.method == 'POST':
        form = CXCForm(request.POST, instance=cxc)
        if form.is_valid():
            form.save()
            # Redirige a la vista de la carpeta asociada a este registro
            return redirect('carpetas:ver_carpeta', carpeta_id=cxc.carpeta.id)
    else:
        form = CXCForm(instance=cxc)
    return render(request, 'control_procesos/editar_cxc.html', {'form': form, 'cxc': cxc})


@login_required
def eliminar_cxc(request, cxc_id):
    """
    Vista para eliminar un registro de CXC.
    Se muestra una confirmación y, al enviar el formulario,
    se elimina el registro.
    """
    cxc = get_object_or_404(CXC, id=cxc_id)
    if request.method == 'POST':
        cxc.delete()
        # Redirige a la vista de la carpeta asociada tras la eliminación
        return redirect('carpetas:ver_carpeta', carpeta_id=cxc.carpeta.id)
    return render(request, 'control_procesos/eliminar_cxc.html', {'cxc': cxc})



################firmas#######################
def crear_firma(request, carpeta_id):
    """
    Vista para crear un nuevo registro de firma en la carpeta especificada.
    """
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        form = RegistroFirmaForm(request.POST)
        if form.is_valid():
            firma = form.save(commit=False)
            firma.carpeta = carpeta
            firma.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = RegistroFirmaForm()
    return render(request, 'control_procesos/crear_firma.html', {'form': form, 'carpeta': carpeta})

def editar_firma(request, firma_id):
    """
    Vista para editar un registro de firma existente.
    """
    firma = get_object_or_404(RegistroFirma, id=firma_id)
    if request.method == 'POST':
        form = RegistroFirmaForm(request.POST, instance=firma)
        if form.is_valid():
            form.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=firma.carpeta.id)
    else:
        form = RegistroFirmaForm(instance=firma)
    return render(request, 'control_procesos/editar_firma.html', {'form': form, 'firma': firma})

def eliminar_firma(request, firma_id):
    """
    Vista para eliminar un registro de firma.
    """
    firma = get_object_or_404(RegistroFirma, id=firma_id)
    carpeta_id = firma.carpeta.id
    firma.delete()
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)

#######################registrar cuentas ########################3
def crear_cuenta_especial(request, carpeta_id):
    """Crea un nuevo registro de 'Cuenta' en la carpeta especificada."""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        form = RegistroCuentaForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.carpeta = carpeta
            cuenta.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = RegistroCuentaForm()
    return render(request, 'control_procesos/crear_cuenta_especial.html', {
        'carpeta': carpeta,
        'form': form
    })

def editar_cuenta_especial(request, cuenta_id):
    """Edita un registro de 'Cuenta' existente."""
    cuenta = get_object_or_404(RegistroCuenta, id=cuenta_id)
    if request.method == 'POST':
        form = RegistroCuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=cuenta.carpeta.id)
    else:
        form = RegistroCuentaForm(instance=cuenta)
    return render(request, 'control_procesos/editar_cuenta_especial.html', {
        'form': form,
        'cuenta': cuenta
    })

def eliminar_cuenta_especial(request, cuenta_id):
    """Elimina un registro de 'Cuenta'."""
    cuenta = get_object_or_404(RegistroCuenta, id=cuenta_id)
    carpeta_id = cuenta.carpeta.id
    cuenta.delete()
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)


#################### pregunta ###############



def crear_pregunta(request, carpeta_id):
    """Crea un nuevo registro de Pregunta en la carpeta especificada."""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        form = RegistroPreguntaForm(request.POST)
        if form.is_valid():
            pregunta_obj = form.save(commit=False)
            pregunta_obj.carpeta = carpeta
            pregunta_obj.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = RegistroPreguntaForm()
    return render(request, 'control_procesos/crear_pregunta.html', {
        'carpeta': carpeta,
        'form': form
    })

def editar_pregunta(request, pregunta_id):
    """Edita un registro de Pregunta existente."""
    pregunta_obj = get_object_or_404(RegistroPregunta, id=pregunta_id)
    if request.method == 'POST':
        form = RegistroPreguntaForm(request.POST, instance=pregunta_obj)
        if form.is_valid():
            form.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=pregunta_obj.carpeta.id)
    else:
        form = RegistroPreguntaForm(instance=pregunta_obj)
    return render(request, 'control_procesos/editar_pregunta.html', {
        'form': form,
        'pregunta_obj': pregunta_obj
    })

def eliminar_pregunta(request, pregunta_id):
    """Elimina un registro de Pregunta."""
    pregunta_obj = get_object_or_404(RegistroPregunta, id=pregunta_id)
    carpeta_id = pregunta_obj.carpeta.id
    pregunta_obj.delete()
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)


##################Claves Sistemas ################



def crear_claves_sistemas(request, carpeta_id):
    """Crea un nuevo registro de 'Claves Sistemas' en la carpeta especificada."""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        form = RegistroClavesSistemasForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.carpeta = carpeta
            registro.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = RegistroClavesSistemasForm()
    return render(request, 'control_procesos/crear_claves_sistemas.html', {
        'carpeta': carpeta,
        'form': form
    })

def editar_claves_sistemas(request, claves_id):
    """Edita un registro de 'Claves Sistemas'."""
    registro = get_object_or_404(RegistroClavesSistemas, id=claves_id)
    if request.method == 'POST':
        form = RegistroClavesSistemasForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=registro.carpeta.id)
    else:
        form = RegistroClavesSistemasForm(instance=registro)
    return render(request, 'control_procesos/editar_claves_sistemas.html', {
        'form': form,
        'registro': registro
    })

def eliminar_claves_sistemas(request, claves_id):
    """Elimina un registro de 'Claves Sistemas'."""
    registro = get_object_or_404(RegistroClavesSistemas, id=claves_id)
    carpeta_id = registro.carpeta.id
    registro.delete()
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)


###################### sistemas #############################

from django.shortcuts import render, get_object_or_404, redirect
from aplicaciones.carpetas.models import Carpeta
from .models import RegistroSistema
from .forms import RegistroSistemaForm

def crear_sistema(request, carpeta_id):
    """Crea un nuevo registro de Sistema en la carpeta especificada."""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        form = RegistroSistemaForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.carpeta = carpeta
            registro.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = RegistroSistemaForm()
    return render(request, 'control_procesos/crear_sistema.html', {
        'carpeta': carpeta,
        'form': form
    })

def editar_sistema(request, sistema_id):
    """Edita un registro de Sistema existente."""
    registro = get_object_or_404(RegistroSistema, id=sistema_id)
    if request.method == 'POST':
        form = RegistroSistemaForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=registro.carpeta.id)
    else:
        form = RegistroSistemaForm(instance=registro)
    return render(request, 'control_procesos/editar_sistema.html', {
        'form': form,
        'registro': registro
    })

def eliminar_sistema(request, sistema_id):
    """Elimina un registro de Sistema."""
    registro = get_object_or_404(RegistroSistema, id=sistema_id)
    carpeta_id = registro.carpeta.id
    registro.delete()
    return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_id)


#############BANCOS############################
def crear_banco(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == 'POST':
        form = BancoForm(request.POST)
        if form.is_valid():
            banco = form.save(commit=False)
            banco.carpeta = carpeta
            banco.save()
            return redirect('carpetas:ver_carpeta', carpeta.id)
    else:
        form = BancoForm()
    return render(request, 'control_procesos/crear_banco.html', {'form': form, 'carpeta': carpeta})

def editar_banco(request, banco_id):
    banco = get_object_or_404(Banco, id=banco_id)
    if request.method == 'POST':
        form = BancoForm(request.POST, instance=banco)
        if form.is_valid():
            form.save()
            return redirect('carpetas:ver_carpeta', banco.carpeta.id)
    else:
        form = BancoForm(instance=banco)
    return render(request, 'control_procesos/editar_banco.html', {'form': form, 'carpeta': banco.carpeta})

def eliminar_banco(request, banco_id):
    banco = get_object_or_404(Banco, id=banco_id)
    carpeta_id = banco.carpeta.id
    banco.delete()
    return redirect('carpetas:ver_carpeta', carpeta_id)


def marcar_y_ver_carpeta(request, noti_id):
    noti = get_object_or_404(Notificacion, id=noti_id, usuario=request.user)
    noti.leida = True
    noti.save()
    # Obtiene ids
    carpeta_id = noti.proceso.carpeta.id
    proc_id    = noti.proceso.id
    # Construye URL /carpetas/ver/<carpeta_id>/#proc-<proc_id>
    url = reverse('carpetas:ver_carpeta', args=[carpeta_id])
    return redirect(f"{url}#proc-{proc_id}")

from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json


@login_required
@require_POST
def cambiar_estado_ajax(request):
    try:
        payload = json.loads(request.body)
        proc_id = payload.get('id')
        nuevo_estado = payload.get('estado')
        proc = get_object_or_404(Proceso, pk=proc_id)
        # Asumiendo que usas choices en el campo estado:
        opciones = dict(Proceso.ESTADO_CHOICES)
        if nuevo_estado in opciones:
            proc.estado = nuevo_estado
            proc.save()
            return JsonResponse({'status': 'ok'})
    except Exception as e:
        pass
    return JsonResponse({'status': 'error'}, status=400)