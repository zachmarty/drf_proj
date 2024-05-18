from rest_framework.exceptions import ValidationError

from habits.models import Habit

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
        if type(data['related_habit']) != int:
            raise ValidationError(
                detail="Sended type of related habit is not correct"
            )
        if type(data['related_habit']) == int:
            habit = Habit.objects.filter(id = data['related_habit'])
            if habit.exists():
                habit = habit.first()
                if habit.usefull == True:
                    raise ValidationError(
                        detail="Related habit cannot be usefull"
                    )
                data['related_habit'] = habit
            else:
                raise ValidationError(
                    detail="This related habit does not exists"
                )
    else:
        if data["reward"] != None or data["related_habit"] != None:
            raise ValidationError(
                detail="If this habit is pleasant, then it should not have any reward or related pleasant habit"
            )
        if data["publicated"] == True:
            raise ValidationError(detail="Pleasant habits cannot be publicated")
    return data
