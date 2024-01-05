# Используем базовый образ с поддержкой Python
FROM python:3.9-slim

# Создаем не-root пользователя
RUN useradd -ms /bin/bash myuser

# Переключаемся на не-root пользователя
USER myuser

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Команда для запуска микросервиса
CMD ["python", "main.py"]
