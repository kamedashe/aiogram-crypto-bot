# 1. Берем легкий Linux с Python 3.10
FROM python:3.10-slim

# 2. Отключаем создание мусорных файлов pycache (чтобы образ был легче)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Создаем рабочую папку внутри контейнера
WORKDIR /app

# 4. Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь код проекта внутрь
COPY . .

# 6. Команда, которая запустится при старте контейнера
CMD ["python", "main.py"]