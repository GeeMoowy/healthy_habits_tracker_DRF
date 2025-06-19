from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Разрешение, позволяющее только владельцу объекта выполнять действия"""

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ только если пользователь - владелец привычки
        return obj.user == request.user
