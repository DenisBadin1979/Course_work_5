from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name


from habits.apps import HabitsConfig
from habits.views import PlaceViewSet, AwardViewSet, HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView, HabitDestroyAPIView

apps_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"places", PlaceViewSet, basename="places")
router.register(r"awards", AwardViewSet, basename="awards")

urlpatterns = [
    path("habit/create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("habit/", HabitListAPIView.as_view(), name="habit-list"),
    path("habit/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-retrieve"),
    path("habit/update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("habit/delete/<int:pk>/", HabitDestroyAPIView.as_view(), name="habit-delete"),
              ] + router.urls
