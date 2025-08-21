from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet)


urlpatterns = router.urls
