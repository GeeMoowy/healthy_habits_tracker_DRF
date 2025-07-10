# ТРЕКЕР ПРИВЫЧЕК

---

![лого успешной операции](https://mega-u.ru/wp-content/uploads/2022/04/4339820_935xp.jpg)

---
### ОПИСАНИЕ:
### Разработка трекера полезных привычек.
В этом приложении мы будем реализовывать бэкенд часть трекера полезных привычек.

- Настроен CORS, чтобы фронтенд мог подключаться к проекту на развернутом сервере.
- Настроена интеграция с Телеграмом, чтобы отправлять напоминания о выполнении привычки.
- Реализована пагинация для вывода списка привычек.
- Описаны модели User и Habit.
- Все необходимые эндпоинты для работы трекера реализованы (CRUD).
- Настроtyd все необходимые валидаторы. 
- Описаны права доступа.
- Настроены отложенные задачи через Celery.
- Проект покрыты тестами на 83%.

---
![лого успешной операции](https://blog.maxford.ru/upload/000/u1/5/d/python-logo-small.png)
Разработка ведется на языке программирования "PYTHON"

### Установка:
Для работы проекта вам потребуется установленный Docker. https://www.docker.com/products/docker-desktop
1. Выполнить команду:
`git clone git@github.com:GeeMoowy/healthy_habits_tracker_DRF.git` - для копирования проекта из удаленного репозитория.
2. Создайте файл .env в корне проекта на основе примера .env.sample
3. Сборка и запуск контейнеров с помощью команды:
`docker-compose up -d --build`
4. Проверка работы контейнеров командой:
`docker-compose ps`
5. Выполнение миграций:
`docker-compose exec backend python manage.py migrate`
6. Создание суперпользователя:
`docker-compose exec backend python manage.py createsuperuser`
7. Остановка проекта:
`docker-compose down`
Для полной очистки (с удалением томов):
`docker-compose down -v`
8. Проверка работоспособности сервисов:
* Для backend откройте в браузере: 
http://localhost:8000/admin/
* Для db выполните команду
`docker-compose exec db psql -U ваш_пользователь -d ваша_база -c "SELECT 1;"`
* Для Redis проверка связи через redis-cli. Команда:
`docker-compose exec redis redis-cli ping`
* Для celery выполните команду:
`docker-compose logs -f celery`
* Для celery-beat выполните команду:
`docker-compose logs -f celery_beat`

# Деплой Django-проекта на удаленный сервер

## Предварительные требования
- Удаленный сервер с Ubuntu 20.04/22.04
- Установленные Docker и Docker Compose
- Доступ по SSH

## 1. Настройка сервера

### Установка Docker и Docker Compose
```bash
# Установка Docker
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce

# Установка Docker Compose Plugin
sudo apt-get install -y docker-compose-plugin

# Проверка установки
docker --version
docker compose version

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker
```
### Настройка firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```
## 2. Настройка CI/CD (GitHub Actions)

### Добавьте secrets в репозиторий GitHub:
- DOCKER_HUB_USERNAME - ваш логин Docker Hub
- DOCKER_HUB_TOKEN - токен Docker Hub
- SSH_KEY - приватный ключ для доступа к серверу
- SSH_USER - пользователь сервера (обычно root или ubuntu)
- SERVER_IP - IP вашего сервера
- SECRET_KEY - секретный ключ Django

IP Адрес сервера: 89.169.178.213


---
#### АВТОР:
Манютин Вячеслав - студент SkyPro (Python-разработчик)