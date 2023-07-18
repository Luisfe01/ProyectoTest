from django.contrib import admin
from .models import Empleado, Cargo, Proyecto

# custom
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','correo','sueldo','cargo', 'activo')
    search_fields = ('nombre','correo')
    list_filter = ('cargo',)
# Register your models here.
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Cargo)
admin.site.register(Proyecto)