# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения для Django
ENV DJANGO_SETTINGS_MODULE=base.settings
ENV PYTHONUNBUFFERED 1

# Запускаем команду для Django
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "base.wsgi:application"]