import datetime
from celery import shared_task
import requests
from django.conf import settings

from habits.models import Habit
from users.models import User


@shared_task
def send_reminder(user_id):
    user = User.objects.get(id = user_id)
    message = ""
    habits = Habit.objects.filter(user=user, usefull = True)
    rofl = datetime.date.today() - datetime.timedelta(days=5)
    output = datetime.date.today() - rofl  
    print(output)
    print(datetime.timedelta(days=5))
    # if habits.exists():
    #     for habit in habits:
    #         times = habit.last_run
    # requests.get(
    #     url=f"https://api.telegram.org/bot{settings.TELEGRAM_API}/sendMessage",
    #     params={"chat_id": settings.TELEGRAM_CHAT, "text": f"ДАУБИ {rofl}"},
    # )
