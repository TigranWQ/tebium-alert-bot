# TeBium Alert Bot - Dockerfile

FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание необходимых директорий
RUN mkdir -p logs data

# Создание пользователя для безопасности
RUN useradd -m -u 1000 alertbot && \
    chown -R alertbot:alertbot /app

USER alertbot

# Переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Экспорт порта для webhook
EXPOSE 8082

# Команда запуска
CMD ["python", "alert_bot.py"]
