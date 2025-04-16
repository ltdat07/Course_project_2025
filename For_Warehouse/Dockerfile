FROM python:3.10-slim

WORKDIR /app

# Копирование requirements.txt для кэширования
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов
COPY . .

CMD ["python", "bot.py"]
