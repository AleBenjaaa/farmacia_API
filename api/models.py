from django.db import models
from django.contrib.auth.models import User

class Medicamento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente", null=True, blank=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ordenes")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    medicamentos = models.ManyToManyField(Medicamento, through="OrdenMedicamento")

    def __str__(self):
        return f"Orden {self.id} - Cliente: {self.cliente.nombre}"

class OrdenMedicamento(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
