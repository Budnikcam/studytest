# Используйте базовый образ Python
FROM python:3.13.1-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл зависимостей в контейнер
COPY requirements.txt ./

# Установите системные зависимости, если необходимо
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Обновите pip и установите зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
    pip install email-validator

# Скопируйте остальную часть приложения
COPY backend/ ./

# Укажите команду для запуска приложения
CMD ["python", "app.py"]
EXPOSE 5000
