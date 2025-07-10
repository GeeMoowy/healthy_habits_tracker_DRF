from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.services import send_tg_message


User = get_user_model()


class HabitTestCase(APITestCase):
    """Набор тестов для проверки работы API привычек. Тестирует основные CRUD-операции,
    права доступа и фильтрацию привычек."""

    def setUp(self):
        """Инициализация тестовых данных.
        Создает:
        - Двух тестовых пользователей (основного и дополнительного)
        - Две тестовые привычки для основного пользователя
        - Очищает базу от предыдущих данных"""

        Habit.objects.all().delete()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        self.habit1 = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='15:00:00',
            action='Бег',
            time_to_complete=100,
            periodicity_days=1,
            is_pleasant=False,
            is_public=False
        )

        self.habit2 = Habit.objects.create(
            user=self.user,
            place='Парк',
            time='08:00:00',
            action='Медитация',
            time_to_complete=15,
            periodicity_days=2,
            is_pleasant=True,
            is_public=False
        )

    def test_list_habits(self):
        """Тестирование получения списка привычек авторизованным пользователем.
        Проверяет:
        - Код ответа 200 OK
        - Возвращаемое количество привычек
        - Пагинацию (count и results в ответе)
        - Что возвращаются только привычки текущего пользователя"""

        response = self.client.get('/habits/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 2)  # Общее количество
        self.assertEqual(len(response.data['results']), 2)  # Привычек в ответе

    def test_create_habit(self):
        """Тестирование создания новой привычки.
        Проверяет:
        - Код ответа 201 Created при успешном создании
        - Корректность сохранения переданных данных
        - Что привычка привязывается к текущему пользователю"""

        data = {
            'place': 'Дом',
            'time': '15:00:00',
            'action': 'Бег',
            'time_to_complete': 100,
            'periodicity_days': 1,
            'is_pleasant': False
        }

        response = self.client.post(
            '/habits/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(response.data['action'], 'Бег')

    def test_anonymous_user_sees_only_public_habits(self):
        """Тестирование доступа анонимных пользователей к привычкам.
        Проверяет:
        - Что неавторизованные пользователи видят только публичные привычки
        - Приватные привычки не возвращаются в ответе
        - Код ответа 200 OK"""

        # Создаем 3 привычки: 2 публичные, 1 приватную
        Habit.objects.create(
            user=self.user,
            place='Парк',
            time='08:00:00',
            action='Публичная привычка 1',
            is_public=True,
            time_to_complete=100
        )

        Habit.objects.create(
            user=self.user,
            place='Дом',
            time='19:00:00',
            action='Публичная привычка 2',
            is_public=True,
            time_to_complete=100
        )

        Habit.objects.create(
            user=self.user,
            place='Офис',
            time='12:00:00',
            action='Приватная привычка',
            is_public=False,
            time_to_complete=100
        )

        # Разлогиниваемся для имитации неаторизованного пользователя
        self.client.logout()

        response = self.client.get('/habits/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Только 2 публичные привычки

        habit_actions = [habit['action'] for habit in response.data['results']]
        self.assertIn('Публичная привычка 1', habit_actions)
        self.assertIn('Публичная привычка 2', habit_actions)
        self.assertNotIn('Приватная привычка', habit_actions)


class TelegramServiceTest(TestCase):
    """Набор тестов для сервиса отправки сообщений в Telegram.
    Проверяет корректность работы функции send_tg_message"""

    @patch('habits.services.requests.post')
    def test_successful_send(self, mock_post):
        """Тест успешной отправки сообщения"""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = send_tg_message(chat_id=123, message="Test message")

        self.assertTrue(result)
        mock_post.assert_called_once()

    def test_invalid_parameters(self):
        """Тест невалидных параметров"""

        with self.assertLogs(level='ERROR') as log:
            self.assertFalse(send_tg_message(None, "Test"))
            self.assertFalse(send_tg_message(123, ""))
            self.assertFalse(send_tg_message(None, None))

        self.assertEqual(len(log.output), 3)
