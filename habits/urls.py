from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name


from habits.apps import HabitsConfig
from habits.views import PlaceViewSet

apps_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"places", PlaceViewSet, basename='places')

urlpatterns = [] + router.urls
