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

# Создаем файл http_proxy.txt и затем изменяем его владельца
RUN touch http_proxy.txt && chown myuser:myuser http_proxy.txt
RUN touch proxy_check.txt && chown myuser:myuser proxy_check.txt

# Копируем остальные файлы проекта
COPY . .

# Команда для запуска микросервиса
CMD ["python", "main.py"]
