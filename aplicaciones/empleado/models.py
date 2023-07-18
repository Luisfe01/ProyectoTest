from django.db import models
from .managers import EmpleadoManager, ProyectoManager
# Create your models here.
class Proyecto(models.Model):
    nombre_proyecto = models.CharField('Nombre proyecto', max_length=50)
    fecha_inicio = models.DateField('Fecha inicio', auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField('Fecha inicio', auto_now=False, auto_now_add=False)
    objects = ProyectoManager()
    def __str__(self):
        return self.nombre_proyecto
class Cargo(models.Model):
    idcargo = models.BigAutoField(primary_key=True)
    cargo = models.CharField('Cargo', max_length=50, null=True)
    def __str__(self):
        return self.cargo
class Empleado(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    correo = models.CharField('Correo', max_length=100)
    sueldo = models.DecimalField('Sueldo', max_digits=8, decimal_places=2)
    activo = models.BooleanField('Activo')
    cargo = models.ForeignKey(Cargo, on_delete=models.RESTRICT, blank=True)
    proyecto = models.ManyToManyField(Proyecto,blank=True,related_name='proyecto_empleado')

    objects = EmpleadoManager()
    def __str__(self) -> str:
        return self.nombre + ' | '+self.correo+' | '+str(self.activo)
