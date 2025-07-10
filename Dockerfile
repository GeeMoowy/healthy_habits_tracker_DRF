FROM python:3.13

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=1.8.5
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Копируем только файлы зависимостей для кэширования
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . .

# Порт и запуск
EXPOSE 8000
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]