"""
URL configuration for Equipment app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, EquipmentViewSet

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'equipment', EquipmentViewSet, basename='equipment')

urlpatterns = [
    path('', include(router.urls)),
]
