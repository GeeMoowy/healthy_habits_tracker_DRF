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


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериалайзер для эндпоинта регистрации"""

    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name', 'phone_number', 'city']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, data):
        """Валидация ввода пароля"""

        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        """Метод, который удаляет поле 'password_confirmation', создает пользователя с хешированием пароля"""

        validated_data.pop('password_confirmation')
        return User.objects.create_user(**validated_data)
