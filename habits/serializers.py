from rest_framework import serializers

from habits.models import Habit
from habits.validators import TimeValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки"""

    class Meta:
        model = Habit
        exclude = [
            "user",
            "last_update",
            "last_run",
        ]
        extra_kwargs = {
            "reward": {"required": True},
            "related_habit": {"required": True},
            "publicated": {"required": True},
        }
        validators = [TimeValidator(field="running_time")]
