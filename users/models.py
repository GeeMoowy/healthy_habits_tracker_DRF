from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):
    """Модель пользователя, наследованная от абстрактного класса AbstractUser. Хранит информацию о пользователе.
    Авторизация заменена на поле: email"""

    username = None
    email = models.EmailField(unique=True,
                              verbose_name='Email',
                              help_text='Укажите почту')
    avatar = models.ImageField(upload_to='users/avatars/',
                               verbose_name='Фото',
                               null=True,
                               blank=True,
                               help_text='Укажите аватар')
    phone_number = models.CharField(max_length=35,
                                    verbose_name='Телефон',
                                    null=True, blank=True,
                                    help_text='Укажите номер телефона')
    city = models.CharField(max_length=100,
                            verbose_name='Город',
                            null=True,
                            blank=True,
                            help_text='Укажите город')
    tg_chat_id = models.CharField(max_length=50,
                                  verbose_name='Телеграм chat-id',
                                  null=True,
                                  blank=True,
                                  help_text='Укажите Телеграм chat-id')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.email}'
