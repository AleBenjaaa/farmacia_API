from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Medicamento, Cliente, Orden
from .serializers import MedicamentoSerializer, ClienteSerializer, OrdenSerializer

@api_view(['GET', 'POST'])
def medicamento_lista(request):
    if request.method == 'GET':
        medicamentos = Medicamento.objects.all()
        serializer = MedicamentoSerializer(medicamentos, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = MedicamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def medicamento_detalles(request, pk):
    try:
        medicamento = Medicamento.objects.get(pk=pk)
    except Medicamento.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicamentoSerializer(medicamento)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = MedicamentoSerializer(medicamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        if 'stock' in request.data:
            nuevo_stock = request.data['stock']
            if nuevo_stock < 0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            medicamento.stock = nuevo_stock
            medicamento.save()
            return Response(MedicamentoSerializer(medicamento).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        medicamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Cliente Views
@api_view(['GET', 'POST'])
def cliente_lista(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def cliente_detalles(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Orden Views
@api_view(['GET', 'POST'])
def orden_lista(request):
    if request.method == 'GET':
        ordenes = Orden.objects.all()
        serializer = OrdenSerializer(ordenes, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = OrdenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def orden_detalles(request, pk):
    try:
        orden = Orden.objects.get(pk=pk)
    except Orden.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrdenSerializer(orden)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = OrdenSerializer(orden, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        orden.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)