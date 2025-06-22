from django.core.management import call_command
from django.test import TestCase
from users.models import User
import io


class CreateSuperUserCommandTest(TestCase):
    """Тестирование модуля csu.py"""

    def test_creates_superuser_with_email(self):
        """Тестируем успешное создание суперпользователя"""

        out = io.StringIO()
        email = 'admin@example.com'
        password = 'securepassword123'

        call_command('csu', '--email', email, '--password', password, stdout=out)

        # Проверяем что пользователь создан
        user = User.objects.get(email=email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertIn(f'Суперпользователь {email} создан', out.getvalue())
