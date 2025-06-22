import requests
import logging

from config import settings

logger = logging.getLogger(__name__)


def send_tg_message(chat_id, message):
    """Отправляет сообщение пользователю в Telegram через бота.
    Функция выполняет HTTP-запрос к Telegram Bot API для отправки сообщения указанному пользователю.
    Включает обработку ошибок и логирование.
        Аргументы:
            chat_id (int): Идентификатор чата пользователя в Telegram.
                          Должен быть действительным Telegram chat_id
            message (str): Текст сообщения для отправки. Не должен быть пустым

        Возвращает результат операции отправки:
            - True: сообщение успешно отправлено
            - False: произошла ошибка при отправке"""

    if not chat_id or not message:
        logger.error(f"Неверные параметры: chat_id={chat_id}, message={message}")
        return False

    url = f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage'
    params = {
        'text': message,
        'chat_id': chat_id
    }

    try:
        response = requests.post(
            url,
            json=params,
            timeout=10  # Таймаут на подключение и чтение (секунды)
        )
        response.raise_for_status()  # Вызовет исключение при статусе 4xx/5xx
        logger.info(f"Сообщение отправлено в chat_id={chat_id}: {message[:50]}...")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка отправки в Telegram: {e}")
        return False
