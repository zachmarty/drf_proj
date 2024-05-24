import datetime
from typing import Any
from rest_framework.exceptions import ValidationError
from habits.models import Habit

class TimeValidator:
    """Валидатор проверки времени выполнения привычки"""
    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        try:
            tmp_val = value[self.field]
        except:
            raise ValidationError("Running time must be attached")
        if tmp_val > 120 * 60:
            raise ValidationError(
                "Running time (in seconds) cannot take more than 2 minutes"
            )
        if tmp_val <= 0:
            raise ValidationError("Put correct running time")

class PeriodValidator:
    """Валидатор проверки выполнения привычки не чаще чем раз в 7 дней"""
    def __init__(self, field) -> None:
        self.field = field

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        try:
            tmp_val = value[self.field]
        except:
            raise ValidationError("Period must be attached")
        if tmp_val < 7:
            raise ValidationError("Period must be more than 6 days")
        if tmp_val > 14:
            raise ValidationError("Period must be lesser than 2 weeks")


def run_time_validator(habit: Habit):
    """Проверка на длительность выполнения привычки"""
    if habit.running_time >= 120:
        raise ValidationError(detail="Running time cannot be more than 120 sec")


def check_input_data(data):
    """Проверка корректности введенной награды за выполнение полезной привычки"""
    if data["usefull"] == True:
        if data["related_habit"] == None and data["reward"] == None:
            raise ValidationError(
                detail="If this habit is usefull, then it should have proper reward or related pleasant habit"
            )
        if data["related_habit"] != None and data["reward"] != None:
            raise ValidationError(
                detail="If this habit is usefull, then it should have only reward or only related pleasant habit"
            )
        if type(data["reward"]) == None:
            if type(data["related_habit"]) != int:
                raise ValidationError(
                    detail="Sended type of related habit is not correct"
                )
            if type(data["related_habit"]) == int:
                habit = Habit.objects.filter(id=data["related_habit"])
                if habit.exists():
                    habit = habit.first()
                    if habit.usefull == True:
                        raise ValidationError(detail="Related habit cannot be usefull")
                    data["related_habit"] = habit
                else:
                    raise ValidationError(detail="This related habit does not exists")
    else:
        if data["reward"] != None or data["related_habit"] != None:
            raise ValidationError(
                detail="If this habit is pleasant, then it should not have any reward or related pleasant habit"
            )
        if data["publicated"] == True:
            raise ValidationError(detail="Pleasant habits cannot be publicated")
    return data
