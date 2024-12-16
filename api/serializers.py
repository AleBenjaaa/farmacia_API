from rest_framework import serializers
from .models import Medicamento, Cliente, Orden, OrdenMedicamento

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class OrdenMedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenMedicamento
        fields = ['medicamento', 'cantidad']

class OrdenSerializer(serializers.ModelSerializer):
    medicamentos = OrdenMedicamentoSerializer(many=True, write_only=True)

    class Meta:
        model = Orden
        fields = ['id', 'cliente', 'fecha', 'total', 'medicamentos']
        read_only_fields = ['total']  # El campo total será calculado automáticamente

    def create(self, validated_data):
        medicamentos_data = validated_data.pop('medicamentos')  # Extraer los medicamentos
        total = 0

        # Calcular el total de la orden
        for medicamento in medicamentos_data:
            medicamento_obj = Medicamento.objects.get(id=medicamento['medicamento'].id)
            total += medicamento_obj.precio * medicamento['cantidad']

        # Crear la orden con el total calculado
        orden = Orden.objects.create(total=total, **validated_data)

        # Crear relaciones en la tabla intermedia OrdenMedicamento
        for medicamento in medicamentos_data:
            OrdenMedicamento.objects.create(
                orden=orden,
                medicamento=medicamento['medicamento'],
                cantidad=medicamento['cantidad']
            )

        return orden
