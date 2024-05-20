from typing import Any
from rest_framework.exceptions import ValidationError

from habits.models import Habit


class TimeValidator:
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


def check_input_data(data):
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
