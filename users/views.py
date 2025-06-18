from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    """Контроллер для пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Метод для определения прав доступа пользователя в зависимости от выбранного действия"""
        if self.action == "create":
            permission_classes = [AllowAny]  # Разрешаем создавать пользователя без аутентификации
        else:
            permission_classes = [IsAuthenticated]  # Для всех остальных действий нужна аутентификация
        return [permission() for permission in permission_classes]
