import asyncio
import logging
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, TelegramObject, Update

from config import TOKEN
from handlers import common, courses, directions, earning_ways, start

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AntiSpamMiddleware(BaseMiddleware):
    """Middleware для защиты от спама и логирования."""

    def __init__(self):
        super().__init__()
        self.spam_keywords = [
            'casino', 'bonus', 'jetacas', 'welcome1k',
            'deposit', 'promo code', 'online casino',
            'bet', 'gambling', 'poker', '$1000', 'claim',
            'withdraw', 'payout', 'betting', 'jackpot'
        ]
        self.blocked_users = set()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Update) and event.message:
            user_id = event.message.from_user.id
            username = event.message.from_user.username
            text = event.message.text or ""

            # Логируем все сообщения
            logger.info(f"Сообщение от {user_id} (@{username}): {text[:100]}...")

            # Проверяем на спам
            if any(keyword.lower() in text.lower() for keyword in self.spam_keywords):
                logger.warning(f"🚨 СПАМ обнаружен от пользователя {user_id} (@{username}): {text}")
                self.blocked_users.add(user_id)

                try:
                    await event.message.reply("❌ Спам обнаружен. Пользователь заблокирован.")
                except Exception as e:
                    logger.error(f"Ошибка при блокировке спама: {e}")
                return

            # Проверяем заблокированных пользователей
            if user_id in self.blocked_users:
                logger.warning(f"🚫 Заблокированный пользователь {user_id} пытается писать")
                return

        return await handler(event, data)


async def main():
    """Главная функция запуска бота."""
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Добавляем антиспам middleware
    dp.message.middleware(AntiSpamMiddleware())

    # Подключаем роутеры из разных модулей - ВАЖЕН ПОРЯДОК!
    dp.include_router(directions.router)
    dp.include_router(courses.router)
    dp.include_router(earning_ways.router)
    dp.include_router(common.router)
    dp.include_router(start.router)  # catch-all в самом конце!

    # Создаем необходимые директории
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("images/main").mkdir(parents=True, exist_ok=True)
    Path("images/directions").mkdir(parents=True, exist_ok=True)
    Path("images/courses").mkdir(parents=True, exist_ok=True)

    logger.info("Бот запускается...")
    logger.info(f"Токен бота: {TOKEN[:10]}...{TOKEN[-10:]}")  # Логируем часть токена для проверки

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
