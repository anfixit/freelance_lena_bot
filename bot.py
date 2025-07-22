import asyncio
import logging
import json
from typing import Dict, Any
from pathlib import Path

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# States для FSM
class UserStates(StatesGroup):
    choosing_profession = State()
    viewing_profession = State()
    viewing_courses = State()
    viewing_earning_ways = State()
    viewing_job_search = State()
    settings = State()

# Загрузка данных профессий
def load_professions() -> list:
    try:
        with open('data/professions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Файл professions.json не найден")
        return []
    except json.JSONDecodeError:
        logger.error("Ошибка при чтении professions.json")
        return []

PROFESSIONS = load_professions()

# Основное меню
def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💼 Каталог профессий"), KeyboardButton(text="📚 Обучающие курсы")],
            [KeyboardButton(text="💰 Способы заработка"), KeyboardButton(text="🔍 Поиск работы")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Инлайн клавиатура для профессий
def get_professions_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for profession in PROFESSIONS:
        buttons.append([InlineKeyboardButton(
            text=f"{profession['emoji']} {profession['title']}",
            callback_data=f"prof_{profession['id']}"
        )])
    buttons.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Детальная клавиатура для профессии
def get_profession_detail_keyboard(prof_id: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📚 Курсы и обучение", callback_data=f"courses_{prof_id}")],
        [InlineKeyboardButton(text="💰 Уровни заработка", callback_data=f"earning_{prof_id}")],
        [InlineKeyboardButton(text="🔍 Где искать работу", callback_data=f"jobsearch_{prof_id}")],
        [InlineKeyboardButton(text="🛠 Инструменты", callback_data=f"tools_{prof_id}")],
        [InlineKeyboardButton(text="↩️ Назад к профессиям", callback_data="professions")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🎯 <b>Добро пожаловать в мир фриланса!</b>\n\n"
        "Я помогу тебе найти способы заработка в интернете и на фрилансе! "
        "Выбери интересующий раздел из меню ниже 👇",
        reply_markup=get_main_menu()
    )

# Обработчик кнопки "Каталог профессий"
@router.message(F.text == "💼 Каталог профессий")
async def show_professions(message: Message, state: FSMContext):
    await state.set_state(UserStates.choosing_profession)
    await message.answer(
        "💼 <b>Каталог профессий</b>\n\n"
        "Выбери интересующую профессию, чтобы узнать подробности:",
        reply_markup=get_professions_keyboard()
    )

# Обработчик выбора профессии
@router.callback_query(F.data.startswith("prof_"))
async def show_profession_detail(callback: CallbackQuery, state: FSMContext):
    prof_id = callback.data.split("_", 1)[1]
    profession = next((p for p in PROFESSIONS if p['id'] == prof_id), None)

    if not profession:
        await callback.answer("Профессия не найдена")
        return

    await state.set_state(UserStates.viewing_profession)
    await state.update_data(current_profession=prof_id)

    text = f"{profession['emoji']} <b>{profession['title']}</b>\n\n"
    text += f"📋 <b>Описание:</b> {profession['description']}\n\n"
    text += f"💵 <b>Средний доход:</b> {profession['income']}\n\n"
    text += f"🎓 <b>Необходимые навыки:</b> {profession['skills']}\n\n"
    text += f"🚀 <b>Как начать:</b> {profession['start']}\n\n"
    text += f"🔗 <b>Полезные ресурсы:</b> {profession['resources']}"

    await callback.message.edit_text(
        text,
        reply_markup=get_profession_detail_keyboard(prof_id)
    )
    await callback.answer()

# Обработчик курсов
@router.callback_query(F.data.startswith("courses_"))
async def show_courses(callback: CallbackQuery, state: FSMContext):
    prof_id = callback.data.split("_", 1)[1]
    profession = next((p for p in PROFESSIONS if p['id'] == prof_id), None)

    if not profession:
        await callback.answer("Профессия не найдена")
        return

    courses = profession.get('courses', {})

    text = f"📚 <b>Курсы: {profession['title']}</b>\n\n"
    text += f"🆓 <b>Бесплатные:</b> {courses.get('free', 'Не указано')}\n\n"
    text += f"💎 <b>Платные:</b> {courses.get('paid', 'Не указано')}\n\n"
    text += f"⏱ <b>Длительность:</b> {courses.get('duration', 'Не указано')}\n\n"
    text += f"🎯 <b>Результат:</b> {courses.get('result', 'Не указано')}"

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад к профессии", callback_data=f"prof_{prof_id}")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer()

# Обработчик поиска работы
@router.callback_query(F.data.startswith("jobsearch_"))
async def show_job_search(callback: CallbackQuery, state: FSMContext):
    prof_id = callback.data.split("_", 1)[1]
    profession = next((p for p in PROFESSIONS if p['id'] == prof_id), None)

    if not profession:
        await callback.answer("Профессия не найдена")
        return

    platforms = profession.get('platforms', [])

    text = f"🔍 <b>Поиск работы: {profession['title']}</b>\n\n"
    text += "<b>Платформы для поиска:</b>\n"

    for i, platform in enumerate(platforms, 1):
        text += f"{i}. {platform}\n"

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад к профессии", callback_data=f"prof_{prof_id}")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer()

# Обработчик "Способы заработка"
@router.message(F.text == "💰 Способы заработка")
async def show_earning_ways(message: Message):
    text = "💰 <b>Способы заработка</b>\n\n"
    text += "🚀 <b>Для новичков (0-20,000 руб/мес):</b>\n"
    text += "• Простые задачи по копирайтингу - 500-1000 руб за текст\n"
    text += "• Базовый дизайн карточек - 200-500 руб за карточку\n"
    text += "• Ведение простых соцсетей - 5,000-15,000 руб/мес\n"
    text += "• Настройка простых ботов - 2,000-5,000 руб за бота\n\n"

    text += "💪 <b>Для опытных (20,000-100,000 руб/мес):</b>\n"
    text += "• Комплексные рекламные кампании - 10,000-30,000 руб/проект\n"
    text += "• Профессиональный видеомонтаж - 3,000-10,000 руб/видео\n"
    text += "• Управление маркетплейсами - 20,000-50,000 руб/мес\n"
    text += "• Автоматизация бизнес-процессов - 15,000-40,000 руб/проект\n\n"

    text += "🔥 <b>Для экспертов (100,000+ руб/мес):</b>\n"
    text += "• Собственные обучающие курсы - 50,000-500,000 руб/запуск\n"
    text += "• Консультации и менторство - 5,000-20,000 руб/час\n"
    text += "• Партнерство с крупными брендами - 100,000+ руб/мес\n"
    text += "• Создание собственных продуктов - безлимит"

    await message.answer(text)

# Обработчик "Обучающие курсы"
@router.message(F.text == "📚 Обучающие курсы")
async def show_courses_menu(message: Message):
    text = "📚 <b>Обучающие курсы</b>\n\n"
    text += "Выбери профессию, чтобы увидеть курсы по ней:"

    await message.answer(text, reply_markup=get_professions_keyboard())

# Обработчик "О боте"
@router.message(F.text == "ℹ️ О боте")
async def show_about(message: Message):
    text = "ℹ️ <b>О боте</b>\n\n"
    text += "🎯 Этот бот поможет тебе найти свой путь в мире фриланса и удаленной работы.\n\n"
    text += "<b>Что умеет бот:</b>\n"
    text += "• Показывает 10+ популярных профессий для фриланса\n"
    text += "• Предоставляет информацию о курсах и обучении\n"
    text += "• Помогает найти площадки для поиска работы\n"
    text += "• Показывает уровни заработка\n"
    text += "• Дает практические советы для старта\n\n"
    text += "💬 <b>Поддержка:</b> @freelance_lena_support\n"
    text += "📈 <b>Версия:</b> 1.0"

    await message.answer(text)

# Обработчик кнопки "Назад к профессиям"
@router.callback_query(F.data == "professions")
async def back_to_professions(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.choosing_profession)
    await callback.message.edit_text(
        "💼 <b>Каталог профессий</b>\n\n"
        "Выбери интересующую профессию, чтобы узнать подробности:",
        reply_markup=get_professions_keyboard()
    )
    await callback.answer()

# Обработчик кнопки "В главное меню"
@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "🏠 <b>Главное меню</b>\n\n"
        "Выбери интересующий раздел:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# Обработчик настроек (заглушка)
@router.message(F.text == "⚙️ Настройки")
async def show_settings(message: Message):
    await message.answer(
        "⚙️ <b>Настройки</b>\n\n"
        "🎯 Выбор интересующих профессий\n"
        "📊 Уровень опыта\n"
        "🔔 Уведомления\n"
        "👤 Профиль\n\n"
        "⚠️ <i>Функционал настроек будет добавлен в следующих версиях</i>"
    )

# Обработчик поиска работы из главного меню
@router.message(F.text == "🔍 Поиск работы")
async def show_job_search_menu(message: Message):
    text = "🔍 <b>Поиск работы</b>\n\n"
    text += "Выбери профессию, чтобы увидеть площадки для поиска работы:"

    await message.answer(text, reply_markup=get_professions_keyboard())

# Обработчик инструментов
@router.callback_query(F.data.startswith("tools_"))
async def show_tools(callback: CallbackQuery):
    prof_id = callback.data.split("_", 1)[1]
    profession = next((p for p in PROFESSIONS if p['id'] == prof_id), None)

    if not profession:
        await callback.answer("Профессия не найдена")
        return

    text = f"🛠 <b>Инструменты: {profession['title']}</b>\n\n"

    # Инструменты в зависимости от профессии
    tools_map = {
        "target_vk": "• Рекламный кабинет ВКонтакте\n• Яндекс.Метрика\n• Google Analytics\n• Контекстная реклама",
        "wb_ozon_design": "• Adobe Photoshop\n• Canva Pro\n• Figma\n• Adobe Illustrator\n• Readymag",
        "video_montage": "• Adobe Premiere Pro\n• After Effects\n• DaVinci Resolve\n• Final Cut Pro\n• Motion Graphics",
        "telegram_promo": "• Telegram Analytics Bot\n• TGStat\n• Telemetr\n• SMMplaner\n• Контент-планировщики",
        "smm_manager": "• SMMplaner\n• Hootsuite\n• Buffer\n• Canva\n• Планировщики контента",
        "china_buying": "• 1688.com\n• Alibaba\n• Переводчики (Google, Яндекс)\n• Калькуляторы доставки",
        "story_sales": "• Instagram Creator Studio\n• Stories Templates\n• Canva\n• Unfold\n• StoryArt",
        "chatbot_specialist": "• Manychat\n• Botmother\n• Chatfuel\n• SendPulse\n• Telegram Bot API",
        "copywriter": "• Grammarly\n• Главред\n• Advego Plagiatus\n• SEO-анализаторы\n• Google Docs",
        "marketplace_manager": "• Личные кабинеты WB/OZON\n• MPStats\n• Wildberries Analytics\n• SellerTools\n• Аналитика продаж"
    }

    text += tools_map.get(prof_id, "Список инструментов формируется...")

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад к профессии", callback_data=f"prof_{prof_id}")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer()

# Обработчик уровней заработка
@router.callback_query(F.data.startswith("earning_"))
async def show_earning_levels(callback: CallbackQuery):
    prof_id = callback.data.split("_", 1)[1]
    profession = next((p for p in PROFESSIONS if p['id'] == prof_id), None)

    if not profession:
        await callback.answer("Профессия не найдена")
        return

    text = f"💰 <b>Уровни заработка: {profession['title']}</b>\n\n"
    text += f"📊 <b>Средний доход:</b> {profession['income']}\n\n"

    # Детальная разбивка по уровням
    earning_details = {
        "target_vk": "🚀 Новичок: 15,000-25,000 руб/мес\n💪 Опытный: 25,000-40,000 руб/мес\n🔥 Эксперт: 40,000+ руб/мес",
        "wb_ozon_design": "🚀 Новичок: 20,000-35,000 руб/мес\n💪 Опытный: 35,000-60,000 руб/мес\n🔥 Эксперт: 60,000+ руб/мес",
        "video_montage": "🚀 Новичок: 25,000-45,000 руб/мес\n💪 Опытный: 45,000-80,000 руб/мес\n🔥 Эксперт: 80,000+ руб/мес",
        "telegram_promo": "🚀 Новичок: 18,000-30,000 руб/мес\n💪 Опытный: 30,000-50,000 руб/мес\n🔥 Эксперт: 50,000+ руб/мес",
        "smm_manager": "🚀 Новичок: 20,000-40,000 руб/мес\n💪 Опытный: 40,000-70,000 руб/мес\n🔥 Эксперт: 70,000+ руб/мес"
    }

    text += earning_details.get(prof_id, "Детальная информация формируется...")

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад к профессии", callback_data=f"prof_{prof_id}")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ])

    await callback.message.edit_text(text, reply_markup=back_keyboard)
    await callback.answer()

# Обработчик неизвестных сообщений
@router.message()
async def unknown_message(message: Message):
    await message.answer(
        "🤔 Не понял твое сообщение.\n\n"
        "Используй кнопки меню для навигации или отправь /start для перезапуска бота."
    )

# Основная функция
async def main():
    # Регистрируем роутер
    dp.include_router(router)

    # Создаем папку data если её нет
    Path("data").mkdir(exist_ok=True)

    logger.info("Бот запускается...")

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
