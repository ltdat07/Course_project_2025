# Используем официальный минимальный образ Python 3.10
FROM python:3.10-slim

# Записываем логи Python сразу (без буферизации)
ENV PYTHONUNBUFFERED=1

# Обновляем пакеты и устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libssl-dev \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Определяем рабочую директорию внутри контейнера
WORKDIR /app

# Сначала копируем requirements.txt, чтобы Docker мог кешировать слои, если зависимости не менялись
COPY requirements.txt .

# Обновляем pip и устанавливаем пакеты из requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Теперь копируем весь остальной код проекта
COPY . /app

# Если нужно собрать расширения (Cython и т.д.), 
# они будут подтянуты при установке из requirements.txt, 
# так как необходимые системные пакеты уже добавлены выше.

# По умолчанию запускать скрипт бота
CMD ["python", "bot.py"]
