from django.urls import path
from rest_framework import routers
from apps.tasks_management.views import TaskManagerView

router = routers.SimpleRouter()
router.register(r'tasks', TaskManagerView)
urlpatterns = router.urls