# Базовый образ с Python 3.12
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=application.settings

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем директории для статики и медиа
RUN mkdir -p /app/static /app/media

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]