import datetime
from celery import shared_task
import requests
from django.conf import settings

from habits.models import Habit
from users.models import User


@shared_task
def send_reminder(user_id):
    """Задача на отправку напоминания о всех привычках, которые нужно выполнить сегодня"""
    user = User.objects.get(id=user_id)
    message = "Сегодня надо выполнить:\n"
    habits = Habit.objects.filter(user=user, usefull=True)
    rofl = datetime.date.today() - datetime.timedelta(days=5)
    output = datetime.date.today() - rofl
    print(output)
    print(datetime.timedelta(days=5))
    if habits.exists():
        for habit in habits:
            times: datetime.timedelta = datetime.date.today() - habit.last_run
            if int(times.days) == int(habit.period):
                message += f"Надо выполнить {habit.action} в {habit.start_time} в {habit.place}"
        if message != "Сегодня надо выполнить:\n":
            requests.get(
                url=f"https://api.telegram.org/bot{settings.TELEGRAM_API}/sendMessage",
                params={
                    "chat_id": settings.TELEGRAM_CHAT,
                    "text": f"Напоминание!!\n{message}",
                },
            )
