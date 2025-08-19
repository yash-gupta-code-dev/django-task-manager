from django.urls import path
from rest_framework import routers
from apps.tasks_management.views import TaskManagerView, TaskManagerViewUserFilter

router = routers.SimpleRouter()
router.register(r'tasks', TaskManagerView)
router.register(r'task-user', TaskManagerViewUserFilter, basename='user')
urlpatterns = router.urls