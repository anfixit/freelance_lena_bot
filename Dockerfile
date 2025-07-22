FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Создаем директорию для данных
RUN mkdir -p data

# Копируем данные профессий
COPY data/professions.json data/

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["python", "bot.py"]
