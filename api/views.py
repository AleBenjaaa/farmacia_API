from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Medicamento, Cliente, Orden
from django.contrib.auth import authenticate
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

@api_view(['GET', 'PATCH', 'DELETE'])
def medicamento_detalles(request, pk):
    try:
        medicamento = Medicamento.objects.get(pk=pk)
    except Medicamento.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicamentoSerializer(medicamento)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    if request.method == 'PATCH':
        if 'stock' in request.data:
            nuevo_stock = request.data['stock']
            if nuevo_stock < 0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            medicamento.stock = nuevo_stock
            medicamento.save()
            return Response(MedicamentoSerializer(medicamento).data)
        else:
             serializer = MedicamentoSerializer(medicamento, data=request.data)

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
    
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        cliente = Cliente.objects.get(user=user)
        token, created = Token.objects.get_or_create(user=user)
        serializer = ClienteSerializer(instance=cliente)
        return Response({"token": token.key, "cliente": serializer.data}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def registro(request):
    serializer = ClienteSerializer(data=request.data)

    if serializer.is_valid():
        cliente = serializer.save()

        # Crear token de autenticación
        token = Token.objects.create(user=cliente.user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
