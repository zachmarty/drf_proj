from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        exclude = [
            "user",
        ]
        extra_kwargs = {
            "reward": {"required": True},
            "related_habit": {"required": True},
            "publicated" : {"required":True},
        }

