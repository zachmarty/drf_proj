import json
from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from rest_framework import status

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тест кейсы на привычки"""

    @staticmethod
    def url_retrieve(pk):
        return reverse_lazy("habits:habit-detail", kwargs={"pk": pk})

    def setUp(self) -> None:
        """Создание пользователя для тестов и ссылок"""
        self.url_list = reverse_lazy("habits:habit-list")
        self.url_self = reverse_lazy("habits:self_habits_list")
        user = {
            "email": "test@test.mail.ru",
            "first_name": "test",
            "last_name": "test",
            "is_staff": True,
            "is_superuser": True,
        }
        self.test_user = User.objects.create(**user)
        self.test_user.set_password("12345678")
        self.client.force_authenticate(user=self.test_user)

    def test_habit_list(self):
        """Проверка списка привычек"""
        habit_data = {
            "place": "mconalds",
            "start_time": "01:00:00",
            "action": "eat mchicken",
            "usefull": True,
            "period": 1,
            "reward": "order another",
            "running_time": 10.0,
            "publicated": True,
            "related_habit": None,
        }
        Habit.objects.create(**habit_data)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 3,
                        "place": "mconalds",
                        "start_time": "01:00:00",
                        "action": "eat mchicken",
                        "usefull": True,
                        "period": 1,
                        "reward": "order another",
                        "running_time": 10.0,
                        "publicated": True,
                        "related_habit": None,
                    }
                ],
            },
        )

    def test_habit_retrieve(self):
        """Проверка отображения одной привычки"""
        habit_data = {
            "place": "mconalds",
            "start_time": "01:00:00",
            "action": "eat mchicken",
            "usefull": True,
            "period": 1,
            "reward": "order another",
            "running_time": 10.0,
            "publicated": True,
            "related_habit": None,
        }
        new_habit = Habit.objects.create(**habit_data)
        response = self.client.get(self.url_retrieve(new_habit.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": 4,
                "place": "mconalds",
                "start_time": "01:00:00",
                "action": "eat mchicken",
                "usefull": True,
                "period": 1,
                "reward": "order another",
                "running_time": 10.0,
                "publicated": True,
                "related_habit": None,
            },
        )

    def test_habit_create(self):
        """Проверка создания привычки"""
        habit_data = {
            "place": "mconalds",
            "start_time": "01:00:00",
            "action": "eat mchicken",
            "usefull": True,
            "period": 1,
            "reward": "order another",
            "running_time": 10.0,
            "publicated": True,
            "related_habit": None,
        }
        response = self.client.post(path=self.url_list, data=habit_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "place": "mconalds",
                "start_time": "01:00:00",
                "action": "eat mchicken",
                "usefull": True,
                "period": 1,
                "reward": "order another",
                "running_time": 10.0,
                "publicated": True,
            },
        )
        self.assertTrue(Habit.objects.all().exists())

    def test_habit_update(self):
        """Проверка обновления привычки"""
        habit_data = {
            "place": "mconalds",
            "start_time": "01:00:00",
            "action": "eat mchicken",
            "usefull": True,
            "period": 1,
            "reward": "order another",
            "running_time": 10.0,
            "publicated": True,
            "related_habit": None,
        }
        new_habit = Habit.objects.create(**habit_data)
        upd_data = {
            "place": "kfc",
            "start_time": "01:00:00",
            "action": "eat mchicken",
            "usefull": True,
            "period": 1,
            "reward": "order another",
            "running_time": 10.0,
            "publicated": True,
            "related_habit": None,
        }
        response = self.client.put(
            self.url_retrieve(new_habit.id), data=upd_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": 5,
                "place": "kfc",
                "start_time": "01:00:00",
                "action": "eat mchicken",
                "usefull": True,
                "period": 1,
                "reward": "order another",
                "running_time": 10.0,
                "publicated": True,
                "related_habit": None,
            },
        )

    def test_habit_delete(self):
        """Проверка удаления привычки"""
        habit_data = {
            "place": "mconalds",
            "start_time": "01:00:00",
            "action": "eat mchicken",
            "usefull": True,
            "period": 1,
            "reward": "order another",
            "running_time": 10.0,
            "publicated": True,
            "related_habit": None,
        }
        new_habit = Habit.objects.create(**habit_data)
        response = self.client.delete(self.url_retrieve(new_habit.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.all().exists())

    def test_self_habit_list(self):
        """Проверка списка своих привычек"""
        habit_data = {
            "place": "mconalds",
            "start_time": "01:00:00",
            "action": "eat mchicken",
            "usefull": True,
            "period": 1,
            "reward": "order another",
            "running_time": 10.0,
            "publicated": False,
            "related_habit": None,
        }
        Habit.objects.create(**habit_data, user=self.test_user)
        response = self.client.get(self.url_self)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 6,
                        "place": "mconalds",
                        "start_time": "01:00:00",
                        "action": "eat mchicken",
                        "usefull": True,
                        "period": 1,
                        "reward": "order another",
                        "running_time": 10.0,
                        "publicated": False,
                        "related_habit": None,
                    }
                ],
            },
        )
