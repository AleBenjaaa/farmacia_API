from django.urls import path, include
from .views import medicamento_lista, cliente_lista, orden_lista, medicamento_detalles, cliente_detalles, orden_detalles




urlpatterns = [
    path('medicamentos/', medicamento_lista),
    path('medicamentos/<int:pk>', medicamento_detalles),
    path('clientes/', cliente_lista),
    path('clientes/<int:pk>', cliente_detalles),
    path('ordenes/', orden_lista),
    path('ordenes/<int:pk>', orden_detalles),
]
