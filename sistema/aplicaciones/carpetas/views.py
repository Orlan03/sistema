from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carpeta, Documento
from .forms import CarpetaForm, DocumentoForm
login_required
from django.shortcuts import render
from .models import Carpeta
from aplicaciones.control_procesos.models import Proceso, CuentaPorCobrar, Respuesta
from django.contrib import messages


def listar_carpetas(request):
    # Crear o verificar la carpeta "Informes Periciales Grupo TACAE"
    informes_periciales, created_ip = Carpeta.objects.get_or_create(nombre="Informes Periciales Grupo TACAE", padre=None)

    # Crear o verificar la carpeta "Control de Procesos"
    control_procesos, created_cp = Carpeta.objects.get_or_create(nombre="Control de Procesos", padre=None)
    procesos_pendientes, created_pp = Carpeta.objects.get_or_create(
        nombre="Procesos Pendientes", 
        padre=control_procesos
    )
    procesos_pendientes, created_pp = Carpeta.objects.get_or_create(
        nombre="Respuestas", 
        padre=control_procesos
    )
    procesos_pendientes, created_pp = Carpeta.objects.get_or_create(
        nombre="Cuentas Por Cobrar", 
        padre=control_procesos
    )
    procesos_pendientes, created_pp = Carpeta.objects.get_or_create(
        nombre="CXC TACAE", 
        padre=control_procesos
    )
    
    datos_grupo, _ = Carpeta.objects.get_or_create(nombre="Datos Grupo TACAE", padre=control_procesos)

    # Crear las subcarpetas dentro de "Datos Grupo TACAE"
    firmas, _         = Carpeta.objects.get_or_create(nombre="Firmas", padre=datos_grupo)
    cuentas, _        = Carpeta.objects.get_or_create(nombre="Cuentas", padre=datos_grupo)
    preguntas, _      = Carpeta.objects.get_or_create(nombre="Preguntas", padre=datos_grupo)
    claves, _= Carpeta.objects.get_or_create(nombre="Claves", padre=datos_grupo)
    sistema, _= Carpeta.objects.get_or_create(nombre="Sistema", padre=datos_grupo)
    sistema_judicial, _= Carpeta.objects.get_or_create(nombre="Sistema Judicial", padre=datos_grupo)
    bancos, _         = Carpeta.objects.get_or_create(nombre="Bancos", padre=datos_grupo)
    # Obtener todas las carpetas raíz (las dos principales)
    carpetas = Carpeta.objects.filter(padre=None)

    return render(request, 'carpetas/listar_carpetas.html', {'carpetas': carpetas})


@login_required
def crear_carpeta(request, carpeta_id=None):
    """ Crea una nueva carpeta o subcarpeta dentro de otra carpeta. """
    carpeta_padre = None
    if carpeta_id:
        carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)

    if request.method == 'POST':
        form = CarpetaForm(request.POST)
        if form.is_valid():
            nueva_carpeta = form.save(commit=False)
            nueva_carpeta.padre = carpeta_padre
            nueva_carpeta.save()
            
            # Redirección
            if nueva_carpeta.padre:
                return redirect('carpetas:ver_carpeta', carpeta_id=nueva_carpeta.padre.id)
            else:
                return redirect('carpetas:listar_carpetas')  # carpeta raíz
    else:
        form = CarpetaForm()

    return render(request, 'carpetas/crear_carpeta.html', {
        'form': form,
        'carpeta_padre': carpeta_padre
    })

@login_required
def crear_subcarpeta(request, carpeta_id):
    carpeta_padre = get_object_or_404(Carpeta, id=carpeta_id)
    if request.method == "POST":
        form = CarpetaForm(request.POST)
        if form.is_valid():
            subcarpeta = form.save(commit=False)
            subcarpeta.padre = carpeta_padre  # ✔ Establecer relación con la carpeta padre
            subcarpeta.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta_padre.id)
    else:
        form = CarpetaForm()

    return render(request, 'carpetas/crear_carpeta.html', {'form': form, 'carpeta_padre': carpeta_padre})


@login_required
def subir_documento(request, carpeta_id):
    """Vista para subir documentos a una carpeta"""
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.carpeta = carpeta
            documento.save()
            return redirect('carpetas:ver_carpeta', carpeta_id=carpeta.id)
    else:
        form = DocumentoForm()

    return render(request, 'carpetas/subir_documento.html', {'form': form, 'carpeta': carpeta})




@login_required
def ver_carpeta(request, carpeta_id):
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    subcarpetas = carpeta.subcarpetas.all()
    documentos = carpeta.documentos.all()
    procesos = carpeta.procesos.all()
    # CXC
    cxcs = carpeta.cxcs.all()  # Si tu modelo CXC tiene related_name='cxcs'
    
    # Respuestas y Cuentas
    respuestas = Respuesta.objects.filter(carpeta=carpeta)
    cuentas = CuentaPorCobrar.objects.filter(carpeta=carpeta)
    
    # Totales
    total_cobrado = sum(cuenta.cobro for cuenta in cuentas)
    total_saldo = sum(cuenta.saldo for cuenta in cuentas)
    
    # Función auxiliar para determinar si la carpeta pertenece a la rama "Informes Periciales Grupo TACAE"
    def pertenece_informes(carpeta_obj):
        aux = carpeta_obj
        while aux is not None:
            if "informes periciales grupo tacae" in aux.nombre.lower():
                return True
            aux = aux.padre
        return False

    # Flag que indica si la carpeta (o alguno de sus padres) pertenece a "Informes Periciales Grupo TACAE"
    flag_pertenece_informes = pertenece_informes(carpeta)
    
    return render(request, 'carpetas/ver_carpeta.html', {
        'carpeta': carpeta,
        'subcarpetas': subcarpetas,
        'documentos': documentos,
        'procesos': procesos,
        'cxcs': cxcs,
        'cuentas': cuentas,
        'total_cobrado': total_cobrado,
        'total_saldo': total_saldo,
        'pertenece_informes': flag_pertenece_informes,
        'respuestas': respuestas,  # si los necesitas en el template
    })
    
@login_required
def eliminar_carpeta(request, carpeta_id):
    """
    Elimina la carpeta especificada y redirige al usuario a la carpeta padre
    si existe, o a la lista de carpetas en caso contrario.
    """
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)
    # Guardar el ID de la carpeta padre (si existe)
    padre_id = carpeta.padre.id if carpeta.padre else None
    carpeta.delete()
    messages.success(request, "Carpeta eliminada exitosamente.")
    if padre_id:
        return redirect('carpetas:ver_carpeta', carpeta_id=padre_id)
    else:
        return redirect('carpetas:listar_carpetas')
