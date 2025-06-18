from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import HabitsPagination
from habits.serializers import HabitSerializer


class HabitsViewSet(ModelViewSet):
    """"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def perform_create(self, serializer):
        """Автоматически назначаем текущего пользователя при создании привычки"""

        serializer.save(user=self.request.user)
