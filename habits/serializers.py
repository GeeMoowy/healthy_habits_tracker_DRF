from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    """Сериализатор для модели Habit. Обеспечивает:
    - Валидацию данных привычки
    - Преобразование между моделью и JSON-представлением
    - Добавление вычисляемых полей:
        periodicity_display (SerializerMethodField): Вычисляемое поле для отображения периодичности
        time_to_complete (IntegerField): Время выполнения с валидацией (1-120 минут)
    Методы:
        validate_time_to_complete: Проверка времени выполнения
        get_periodicity_display: Получение читаемого представления периодичности
        validate: Комплексная валидация взаимосвязанных полей"""

    periodicity_display = serializers.SerializerMethodField()
    time_to_complete = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(120)
        ]
    )
    class Meta:
        model = Habit
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'periodicity_days': {
                'min_value': 1,
                'max_value': 7
            }
        }

    def validate_time_to_complete(self, value):
        """Валидация времени выполнения привычки."""

        if value > 120 or value < 1:
            raise serializers.ValidationError("Время выполнения не должно быть меньше минуты или превышать 120 минут")
        return value

    def get_periodicity_display(self, obj):
        """Получение читаемого представления периодичности."""

        return obj.periodicity_display

    def validate(self, data):
        """Комплексная валидация взаимосвязанных полей привычки.
        Проверяет:
        - У приятной привычки не может быть вознаграждения
        - У приятной привычки не может быть связанной привычки
        - Связанная привычка должна быть приятной"""

        is_pleasant = data.get('is_pleasant', False)
        reward = data.get('reward')
        related_habit = data.get('related_habit')

        if is_pleasant and reward:
            raise serializers.ValidationError("У приятной привычки не может быть вознаграждения")

        if is_pleasant and related_habit:
            raise serializers.ValidationError("У приятной привычки не может быть связанной привычки")

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной")

        return data
