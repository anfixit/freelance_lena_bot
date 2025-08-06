from aiogram import F, Router
from aiogram.types import CallbackQuery

from constants import COURSE_BENEFITS, TARIFFS_DESCRIPTION
from keyboards import get_back_to_courses_keyboard, get_tariffs_keyboard
from utils.data_loader import get_direction_by_id, load_directions

router = Router()
DIRECTIONS = load_directions()


@router.callback_query(F.data.startswith("courses_"))
async def show_courses(callback: CallbackQuery):
    """Показать курсы для направления."""
    dir_id = callback.data.split("_", 1)[1]
    direction = get_direction_by_id(DIRECTIONS, dir_id)

    if not direction or 'courses' not in direction:
        await callback.answer("Курсы не найдены")
        return

    text = f"📚 <b>Курсы: {direction['title']}</b>\n\n"

    for course in direction['courses']:
        text += f"🎓 <b>{course['name']}</b>\n"
        text += f"{course['description']}\n\n"
        text += f"💰 <b>Средний доход:</b> {course['income']}\n"
        text += f"💳 <b>Стоимость:</b> {course['price_basic']} без чата помощи\n"
        text += f"💳 <b>С чатом:</b> {course['price_with_chat']}\n\n"
        text += f"{COURSE_BENEFITS}\n\n"
        text += "---\n\n"

    await callback.message.edit_text(text, reply_markup=get_back_to_courses_keyboard(dir_id))
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def show_tariffs(callback: CallbackQuery):
    """Показать тарифы для покупки."""
    text = f"💳 <b>Тарифы обучения</b>\n\n{TARIFFS_DESCRIPTION}"

    await callback.message.edit_text(text, reply_markup=get_tariffs_keyboard())
    await callback.answer()
