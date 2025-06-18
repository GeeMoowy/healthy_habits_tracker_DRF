from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    """"""
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
            'user': {'required': False}
        }

    def validate_time_to_complete(self, value):
        if value > 120 or value < 1:
            raise serializers.ValidationError("Время выполнения не должно быть меньше минуты или превышать 120 минут")
        return value