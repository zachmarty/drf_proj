from typing import Any
from django.core.management import BaseCommand
from habits.tasks import send_reminder
from users.models import User
from rest_framework.exceptions import NotFound

class Command(BaseCommand):
    """Команда для создания суперпользователя"""
    send_reminder(1)
    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            admin = User.objects.get(email="admin@mail.ru")
            admin.delete()
        except:
            raise NotFound("User not found")
        admin = User.objects.create(
            email="admin@mail.ru",
            first_name="admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,
        )
        admin.set_password("12345678")
        admin.save()
