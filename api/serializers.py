from rest_framework import serializers
from .models import Medicamento, Cliente, Orden, OrdenMedicamento
from django.contrib.auth.models import User

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'

class ClienteSerializerA(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono']

class ClienteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', write_only=True)
    password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono', 'username', 'password']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        cliente = Cliente.objects.create(user=user, **validated_data)
        return cliente

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.user.username
        return representation

class OrdenMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenMedicamento
        fields = ['medicamento', 'cantidad']

class OrdenSerializer(serializers.ModelSerializer):
    medicamentos = OrdenMedicamentoSerializer(many=True, write_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'cliente', 'fecha', 'total', 'medicamentos']
        read_only_fields = ['total'] 

    def create(self, validated_data):
        medicamentos_data = validated_data.pop('medicamentos') 
        total = 0

       
        for medicamento in medicamentos_data:
            medicamento_obj = Medicamento.objects.get(id=medicamento['medicamento'].id)
            total += medicamento_obj.precio * medicamento['cantidad']

   
        orden = Orden.objects.create(total=total, **validated_data)


        for medicamento in medicamentos_data:
            OrdenMedicamento.objects.create(
                orden=orden,
                medicamento=medicamento['medicamento'],
                cantidad=medicamento['cantidad']
            )

        return orden
