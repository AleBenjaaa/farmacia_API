from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicamentoViewSet, ClienteViewSet, OrdenViewSet

router = DefaultRouter()
router.register('medicamentos', MedicamentoViewSet)
router.register('clientes', ClienteViewSet)
router.register('ordenes', OrdenViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
