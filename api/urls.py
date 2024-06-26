from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListaTalleresViewSet, AgendamientoViewSet

router = DefaultRouter()
router.register(r'talleres', ListaTalleresViewSet)
router.register(r'agendamientos', AgendamientoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]