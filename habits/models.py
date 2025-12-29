from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits", verbose_name="Пользователь"
    )
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="connected",
        verbose_name="Связанная привычка",
        help_text="Используется только для полезных привычек",
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Периодичность в днях",
        help_text="Как часто выполнять (1 - каждый день, т.е. 7 раз в неделю)",
    )
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name="Вознаграждение")
    duration = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение (в секундах)", help_text="Не должно превышать 120 секунд"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
