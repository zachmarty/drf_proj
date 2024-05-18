from django.urls import path
from habits.apps import HabitsConfig
from rest_framework.routers import DefaultRouter

from habits.views import HabitViewSet, SelfHabitsView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"habit", HabitViewSet, basename="habit")

urlpatterns = [
    path("habit/self", SelfHabitsView.as_view(), name="self_habits_list"),
] + router.urls
