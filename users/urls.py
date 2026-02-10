from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name


from habits.apps import HabitsConfig
from habits.views import PlaceViewSet
from users.apps import UsersConfig
from users.views import UserViewSet

apps_name = UsersConfig.name

router = DefaultRouter()
router.register("users", UserViewSet, basename='users')

urlpatterns = [] + router.urls