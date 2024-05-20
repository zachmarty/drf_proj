from typing import Any
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            admin = User.objects.get(email="admin@mail.ru")
            admin.delete()
        except:
            pass
        admin = User.objects.create(
            email="admin@mail.ru",
            first_name="admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,
        )
        admin.set_password("12345678")
        admin.save()
