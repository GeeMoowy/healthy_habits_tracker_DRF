from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для получения пользователя (User).
    ***
    Создаем поле
    password: - обязательное поле только для записи.
    ***
    Включает отображение основных данных пользователя в полях:
    [id, email, avatar, phone_number, city]"""

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'avatar', 'phone_number', 'city']

    def create(self, validated_data):
        """Создаем нового пользователя с хэшированием пароля"""

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            avatar=validated_data.get('avatar'),
            phone_number=validated_data.get('phone_number'),
            city=validated_data.get('city')
        )
        return user
