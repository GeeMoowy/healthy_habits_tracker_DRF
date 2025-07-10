from django.db.models import Q
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import HabitsPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitsViewSet(ModelViewSet):
    """ViewSet для работы с привычками пользователя. Обеспечивает CRUD операции для привычек с учетом:
    - Авторизации пользователей
    - Разделения доступа к приватным/публичным привычкам
    - Автоматического назначения владельца при создании"""

    serializer_class = HabitSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        """Возвращаем только привычки текущего пользователя
        или публичные привычки других пользователей (только для чтения)"""

        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(Q(user=user) | Q(is_public=True))
        return Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        """Автоматически назначаем текущего пользователя при создании привычки"""

        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Разные права для разных действий:
        - Создание: только авторизованные
        - Просмотр списка: все (но фильтр в get_queryset)
        - Остальные действия: только владелец
        """
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
