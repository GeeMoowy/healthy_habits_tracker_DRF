from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Habit(models.Model):
    """"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь — создатель привычки'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения привычки',
        help_text='Введите место, в котором необходимо выполнять привычку'
    )

    time = models.TimeField(
        verbose_name='Время выполнения привычки',
        help_text='Введите время, когда необходимо выполнять привычку'
    )

    action = models.CharField(
        max_length=255,
        verbose_name='Действие, которое представляет собой привычка',
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки',
        help_text='Отметьте, является ли эта привычка приятной'
    )

    related_habit: Optional['Habit'] = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        related_name='main_habit',
        help_text='Привычка, которая связана с другой привычкой. Указывать только для полезных привычек'
    )

    periodicity_days = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message="Периодичность не может быть меньше 1 дня"),
            MaxValueValidator(7, message="Нельзя выполнять привычку реже чем 1 раз в 7 дней")
        ],
        verbose_name='Периодичность (в днях)',
        help_text='Интервал в днях между выполнениями привычки (1-7 дней)'
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение после выполнения',
        help_text='Чем пользователь должен себя вознаградить после выполнения'
    )

    time_to_complete = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Время выполнения должно быть не менее 1 минуты"),
            MaxValueValidator(120, message="Время выполнения не должно превышать 120 минут")
        ],
        verbose_name='Время на выполнение (в минутах)',
        help_text='Время, которое предположительно потратит пользователь на выполнение привычки (1-120 минут)'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности',
        help_text='Отметьте, можно ли публиковать привычки в общий доступ'
    )

    def __str__(self):
        return f"{self.action} в {self.time} ({self.place})"

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя указывать и связанную привычку, и вознаграждение.")
        if self.is_pleasant and self.related_habit:
            raise ValidationError("У приятной привычки не может быть связанной привычки.")
        if self.is_pleasant and self.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной (is_pleasant=True)")
        if not 1 <= self.periodicity_days <= 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней")

    @property
    def periodicity_display(self):
        if self.periodicity_days == 1:
            return "Ежедневно"
        elif self.periodicity_days == 7:
            return "Еженедельно"
        return f"Каждые {self.periodicity_days} дня(ей)"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
