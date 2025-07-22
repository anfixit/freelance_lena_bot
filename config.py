import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен бота (можно задать через переменную окружения или напрямую)
TOKEN = os.getenv("BOT_TOKEN", "7889941062:AAF90-F0PY5xQWb-CZBndU7JIVr53ArBj7U")

# Настройки базы данных (для будущего использования)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")

# Настройки веб-хука (для продакшена)
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "https://your-domain.com")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))
WEBHOOK_PATH = f"/webhook/{TOKEN.split(':')[0]}"

# Настройки сервера
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# Админы бота
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []

# Режим разработки
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
