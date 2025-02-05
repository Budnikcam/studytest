# Используйте официальный образ Python
FROM python:3.13.1

# Установите рабочую директорию
WORKDIR /backend/app.py

# Скопируйте файл зависимостей в контейнер
COPY requirements.txt ./

# Установите зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Скопируйте остальную часть приложения
COPY . .

# Определите команду для запуска приложения
CMD ["python", "app.py"]
