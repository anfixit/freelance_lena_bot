from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import get_main_menu
from utils.image_handler import get_start_image

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start с картинкой."""
    await state.clear()

    text = ("🎯 <b>Добро пожаловать в мир фриланса!</b>\n\n"
            "Я помогу тебе найти способы заработка в интернете и на фрилансе! "
            "Выбери интересующий раздел из меню ниже 👇")

    try:
        # Пытаемся отправить с картинкой
        photo = get_start_image()
        if photo:
            await message.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=get_main_menu()
            )
        else:
            # Если картинки нет - отправляем обычным текстом
            await message.answer(text, reply_markup=get_main_menu())
    except Exception as e:
        # При любой ошибке - отправляем текстом
        await message.answer(text, reply_markup=get_main_menu())


@router.message()
async def unknown_message(message: Message):
    """Обработчик неизвестных сообщений."""
    await message.answer(
        "🤔 Не понял твое сообщение.\n\n"
        "Используй кнопки меню для навигации или отправь /start для перезапуска бота."
    )
