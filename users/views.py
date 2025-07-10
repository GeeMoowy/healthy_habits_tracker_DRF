from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    """ViewSet для работы с пользователями системы. Обеспечивает следующие функции:
    - Регистрация новых пользователей
    - Просмотр и редактирование профиля
    - Гибкая система прав доступа
    - Кастомный процесс создания пользователя
    Стандартные действия:
    list — список пользователей
    retrieve — детализация пользователя
    create — регистрация нового пользователя
    update/partial_update — редактирование
    destroy — удаление"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Выбираем сериализатор в зависимости от действия"""

        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    def get_permissions(self):
        """Метод для определения прав доступа пользователя в зависимости от выбранного действия"""
        if self.action == "create":
            permission_classes = [AllowAny]  # Разрешаем создавать пользователя без аутентификации
        else:
            permission_classes = [IsAuthenticated]  # Для всех остальных действий нужна аутентификация
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Кастомизация создания пользователя (регистрации)"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно зарегистрирован"
        }, status=status.HTTP_201_CREATED)
