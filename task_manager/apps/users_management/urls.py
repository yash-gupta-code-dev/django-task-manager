from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserManagementViewSet

router = DefaultRouter()
router.register(r'user', UserManagementViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
