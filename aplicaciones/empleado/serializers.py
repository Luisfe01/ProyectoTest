from .models import Empleado, Cargo, Proyecto
from rest_framework import serializers
import re
from rest_framework.validators import UniqueValidator
class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ('nombre', 'correo', 'sueldo', 'activo', 'cargo', 'proyecto')
        extra_kwargs = {
            'nombre':{'error_messages': {'blank': 'El nombre no puede estar vacio'}},
            'sueldo':{'error_messages': {'invalid': 'El sueldo no puede estar vacio'}},
            'correo':{'validators':[UniqueValidator(queryset=Empleado.objects.all())]}
        }
    def validate_sueldo(self, value):
        if value<=0:
            raise serializers.ValidationError('El sueldo no es valido')
        return value

    def validate_correo(self, value):
        regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        # altregex = r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$"
        if not re.search(regex, value):
            raise serializers.ValidationError('Correo no valido')
        return value
    
    def validate(self, data):
        if data['nombre']==data['correo']:
            raise serializers.ValidationError('El nombre no puede ser igual al correo')
        return data
    
class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('__all__')

class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ('__all__')


class EmpleadoCPSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer()
    proyecto = ProyectoSerializer(many=True)
    class Meta:
        model = Empleado
        fields =  ('id', 'nombre', 'correo', 'sueldo', 'activo', 'cargo', 'proyecto')

class ProyectoSerializerFecha(serializers.Serializer):
    proyecto_empleado = serializers.CharField()
    proyecto_empleado__nombre = serializers.CharField()
    nombre_proyecto = serializers.CharField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()

class ProyectoSerializerResumen(serializers.Serializer):
    nombre_proyecto = serializers.CharField()
    monto = serializers.DecimalField(max_digits=8, decimal_places=2)
    cant = serializers.IntegerField()