from django.db import models
from aplicaciones.carpetas.models import Carpeta
from django.contrib.auth.models import User

class Proceso(models.Model):
    sorteo = models.DateField(blank=True, null=True)
    proceso = models.CharField(max_length=200)
    # Se cambia responsable a ForeignKey al modelo User
    responsable = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Responsable"
    )
    calificacion = models.CharField(max_length=100, blank=True, null=True)
    actor = models.CharField(max_length=200, default="Desconocido")
    demandado = models.CharField(max_length=200, default="Desconocido")
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    posesion = models.CharField(max_length=100, blank=True, null=True)
    fecha_cumplimiento = models.DateField(blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    # Definir las opciones para el campo estado
    ESTADO_CHOICES = (
        ('hecho', 'Hecho'),
        ('pendiente', 'Pendiente'),
        ('faltan_datos', 'Faltan datos'),
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente'
    )
    
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name='procesos')

    def __str__(self):
        return self.proceso
    
    
#####hecho, pendiente, faltan datos


class Respuesta(models.Model):
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name="respuestas")
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name="respuestas", null=True, blank=True)
    fecha_respuesta = models.DateField()
    calificacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_cumplimiento = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Respuesta de {self.proceso} - {self.fecha_respuesta}"
    


class CuentaPorCobrar(models.Model):
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name="cuentas_por_cobrar")
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, related_name="cuentas_cobrar")
    cobro = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    observacion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Asegura que el saldo siempre sea actualizado correctamente"""
        self.saldo = self.proceso.valor - self.cobro  # Restar cobro al valor total
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.proceso.proceso} - {self.cobro}"



class CXC(models.Model):
    carpeta = models.ForeignKey(
        Carpeta, 
        on_delete=models.CASCADE,
        related_name='cxcs',  # Para acceder a las CXC desde la carpeta usando carpeta.cxcs.all()
        null=True, 
        blank=True
    )
    cliente = models.CharField(max_length=255, blank=True, null=True)
    numero_factura = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.CharField(max_length=255, blank=True, null=True)  # o DateField
    real = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cliente or 'Sin Cliente'} - {self.numero_factura or 'Sin Factura'}"



class RegistroFirma(models.Model):
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name='firmas')
    perito = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20)
    clave = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.perito} - {self.ruc}"
    
    


class RegistroCuenta(models.Model):
    carpeta = models.ForeignKey(
        Carpeta,
        on_delete=models.CASCADE,
        related_name='cuentasEspeciales'  # Ajusta el nombre según tu preferencia
    )
    compania = models.CharField(max_length=100, blank=True, null=True)
    institucion_financiera = models.CharField(max_length=150, blank=True, null=True)
    numero = models.CharField(max_length=50, blank=True, null=True)
    ruc_ci = models.CharField(max_length=20, blank=True, null=True)
    usuario = models.CharField(max_length=50, blank=True, null=True)
    clave_web = models.CharField(max_length=100, blank=True, null=True)
    clave_cajero = models.CharField(max_length=100, blank=True, null=True)
    clave_trush = models.CharField(max_length=100, blank=True, null=True)
    clave_sut = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.compania or 'Sin Compañía'} - {self.institucion_financiera or 'Sin Institución'}"

class RegistroPregunta(models.Model):
    carpeta = models.ForeignKey(
        Carpeta,
        on_delete=models.CASCADE,
        related_name='preguntasEspeciales'  
    )
    pregunta = models.TextField()
    respuesta = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.pregunta[:30]}..."
    
class RegistroClavesSistemas(models.Model):
    carpeta = models.ForeignKey(
        Carpeta,
        on_delete=models.CASCADE,
        related_name='clavesSistemas'  # Ajusta el related_name según prefieras
    )
    compania = models.CharField(max_length=200, blank=True, null=True)
    canton = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    clave_mail = models.CharField(max_length=100, blank=True, null=True)
    fecha_declaracion = models.DateField(blank=True, null=True)
    declaracion = models.CharField(max_length=100, blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True, null=True)
    clave_sri = models.CharField(max_length=100, blank=True, null=True)
    clave_super = models.CharField(max_length=100, blank=True, null=True)
    clave_iess = models.CharField(max_length=100, blank=True, null=True)
    perito_judicial = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.compania or 'Sin Compañía'} - {self.ruc or 'Sin RUC'}"
    
    
class RegistroSistema(models.Model):
    carpeta = models.ForeignKey(
        Carpeta,
        on_delete=models.CASCADE,
        related_name='sistemasEspeciales'  # Ajusta el related_name a tu gusto
    )
    compania = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    clave = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.compania or 'Sin Compañía'} - {self.usuario or 'Sin Usuario'}"   


class Banco(models.Model):
    compania = models.CharField(max_length=100)
    institucion_financiera = models.CharField(max_length=100)
    numero = models.CharField(max_length=50)
    ruc_ci = models.CharField(max_length=20)
    usuario = models.CharField(max_length=100)
    clave_web = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name='bancos')

    def __str__(self):
        return f"{self.compania} - {self.institucion_financiera}"

class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notificaciones_control")
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.CharField(max_length=255)
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Opcionalmente, un campo para distinguir el tipo de notificación
    tipo = models.CharField(max_length=50, default="general")

    def __str__(self):
        return self.mensaje