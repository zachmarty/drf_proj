from django.db import models

from users.models import User


# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    start_time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=100, verbose_name="Действие")
    usefull = models.BooleanField(verbose_name="Признак полезной привычки")
    related_habit = models.ForeignKey(
        "self",
        verbose_name="Связная полезная привычка",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    period = models.IntegerField(default=1, verbose_name="Интервал")
    reward = models.CharField(max_length=100, verbose_name="Вознагрождение", null=True)
    running_time = models.FloatField(verbose_name="Время выполнения")
    publicated = models.BooleanField(default=False, verbose_name="Признак публикации")
    last_update = models.DateTimeField(verbose_name='Последнее обновление', blank=True, null=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = [
            "user",
        ]
