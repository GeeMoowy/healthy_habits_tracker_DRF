from celery import shared_task
from django.utils import timezone
import logging

from habits.models import Habit
from habits.services import send_tg_message

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder():
    """Периодическая задача Celery для отправки напоминаний о привычках в Telegram.

    Задача выполняет следующие действия:
    1. Получает текущее локальное время с учетом часового пояса
    2. Находит все привычки, запланированные на текущее время
    3. Формирует и отправляет персонализированные сообщения в Telegram
    4. Логирует результаты выполнения

    Формирует строку с отчетом о количестве отправленных напоминаний в формате:'Отправлено X напоминаний'"""

    now = timezone.localtime()
    current_time = now.time()

    logger.info(f'Запуск проверки привычек {now}')

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    )

    logger.info(f'Найдено {habits.count()} привычек для напоминания')

    for habit in habits:
        message = f"⏰ Напоминание о привычке!\n\n" \
                 f"Действие: {habit.action}\n" \
                 f"Место: {habit.place}\n" \
                 f"Время выполнения: {habit.time.strftime('%H:%M')}\n" \
                 f"Награда: {habit.reward or 'нет'}"

        if habit.user.tg_chat_id:
            send_tg_message(habit.user.tg_chat_id, message)
            logger.info(f'Отправлено напоминание в телеграм пользователю {habit.user}')
        else:
            logger.warning(f"У пользователя {habit.user} не указан tg_chat_id")

    return f"Отправлено {habits.count()} напоминаний"
