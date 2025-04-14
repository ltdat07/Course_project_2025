FROM python:3.10-slim

# Указываем рабочую директорию
WORKDIR /app

# Копируем список зависимостей
COPY requirements.txt .

COPY ESP_sklad_2.xlsx .

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/For_Warehouse
COPY ESP_sklad_2.xlsx /app/For_Warehouse/ESP_sklad_2.xlsx

# Копируем все файлы из текущей папки в контейнер
COPY . .

# Запускаем бота
CMD ["python", "bot.py"]
