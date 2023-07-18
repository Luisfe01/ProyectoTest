from django.shortcuts import render
from .models import Cargo, Empleado
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import EmpleadoForm
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# CREANDO API VIEWS
from rest_framework.generics import (ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, GenericAPIView)
from .serializers import EmpleadoSerializer
from .serializers import EmpleadoCPSerializer
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto
from .serializers import ProyectoSerializerFecha, ProyectoSerializerResumen
import copy
from rest_framework.permissions import (BasePermission, IsAuthenticated, DjangoModelPermissions)




# class EliminarAPIEmpleadoID(DestroyModelMixin, GenericAPIView):
#     serializer_class = EmpleadoDeleteSerializer
#     queryset = Empleado.objects.all()

#     def delete


# CUSTOM GET PERMISION

class CustomDjangoModelPermission(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map) #From EunChong's answer
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


# GET: OBTENER TODA LA LISTA DE EMPELADO
class ListaAPIEmpleado(ListAPIView):
    permission_classes = [CustomDjangoModelPermission]
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.all()

# GET Y OBTENIENDO EL CARGO Y PROYECTO DE CADA EMPLEADO
class ListaAPIEmpleado2(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmpleadoCPSerializer
    queryset = Empleado.objects.all()

# POST PARA CREAR EMPLEADO NUEVO
class CrearAPIEmpleado(CreateAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


# GET Y OBTENIENDO EL EMPLEADO INDIVIDUALMENTE POR EL ID
class ObtenerAPiEmpleado(RetrieveAPIView):
    serializer_class = EmpleadoCPSerializer
    queryset = Empleado.objects.all()


# PUT PARA MODIFICAR UN EMPLEADO

class ModificarAPIEmpleado(UpdateAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.all()
    
# SE LE PUEDEN HACER PETICIONES GET O PUT. TRAE LOS DATOS EXISTENTES DEL EMPLEADO
class ModificarAPIEmpleado2(RetrieveUpdateAPIView):
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.all()


# DELETE / BORRAR
# class EliminarAPIEmpleado(DestroyAPIView):
#     serializer_class = EmpleadoSerializer
#     queryset = Empleado.objects.all()

# MISMO METODO DE ARRIBA SOLAMENTE QUE FUE MODIFICADO PARA PERMITIR CAMBIAR EL ESTADO DE UN EMPLEADO EN LUGAR DE ELIMINARLO
class EliminarAPIEmpleado(DestroyAPIView):
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.all()


    def destroy(self, request, *args, **kwargs):
        emp = self.get_object()
        emp.activo = False
        emp.save()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            print()
        else:
            pass
        
        return Response(
            {'empleado':EmpleadoSerializer(self.get_object()).data,'exito':'sí'},
            status=status.HTTP_204_NO_CONTENT
        )
# API PARA VER LOS EMPLEADOS QUE COINCIDAN CON UN CORREO O NOMBRE ESPECIFICO PASADO COMO PARAMETRO EN LA URL
class BuscarAPIEmpleados(ListAPIView):
    serializer_class = EmpleadoCPSerializer

    def get_queryset(self):
        texto = self.kwargs['texto']
        return Empleado.objects.buscar_empleados(texto)

# API PARA PARA BUSCAR POR EMPLEADOS ENTRE UN SUELDO MINIMO Y MAXIMO Y LOS ORDENA DE MAYOR A MENOR POR EL ORDER BY CONFIGURADO EN EL MANAGER
class BuscarAPIEmpleadosSueldo(ListAPIView):
    serializer_class = EmpleadoCPSerializer

    def get_queryset(self):
        mini = self.kwargs['mini']
        maxi = self.kwargs['maxi']

        return (Empleado.objects.buscar_empleados_sueldo(mini,maxi))

# LISTAR PROYECTOS POR FECHA
class ListaAPIProyectos(ListAPIView):
    serializer_class = ProyectoSerializerFecha

    def get_queryset(self):
        f1 = self.request.query_params.get('fecha1')
        f2 = self.request.query_params.get('fecha2')

        return (Proyecto.objects.lista_proyectos(f1,f2))

# LISTAR SUELDOS DEL PROYECTO Y CANTIDAD DE EMPLEADOS DE ESTOS

class ResumeAPIProyectos(ListAPIView):
    serializer_class= ProyectoSerializerResumen
    queryset = Proyecto.objects.resumen_proyectos()

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ModificarEmpleado(PermissionRequiredMixin, UpdateView):
    permission_required = ('empleado.change_empleado',)
    template_name = 'empleado/modificar-empleado.html'
    model = Empleado
    form_class = EmpleadoForm
    success_url = reverse_lazy('empleados_app:listar-empleados')

@method_decorator(login_required, name='dispatch')
class ListarEmpleados(ListView):
    template_name = 'empleado/listar-empleados.html'
    model = Empleado
    context_object_name = 'lista_empleados'
    queryset = Empleado.objects.filter(activo=True)
    paginate_by = 3

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        lista = Empleado.objects.filter(activo=True)
        if buscar:
            lista = Empleado.objects.filter(nombre__icontains=buscar)
        return lista

class CrearEmpleado(LoginRequiredMixin, CreateView):
    template_name = 'empleado/crear-empleado.html'
    model = Empleado
    fields = ['nombre','correo','sueldo','activo','cargo']
    success_url = reverse_lazy('empleados_app:listar-empleados')

class CrearEmpleado2(CreateView):
    template_name = 'empleado/crear-empleado.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('empleados_app:listar-empleados')

class EliminarEmpleado(DeleteView):
    template_name = 'empleado/eliminar-empleado.html'
    model = Empleado
    success_url = reverse_lazy('empleados_app:listar-empleados')