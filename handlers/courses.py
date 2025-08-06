from aiogram import F, Router
from aiogram.types import CallbackQuery

from constants import COURSE_BENEFITS, TARIFFS_DESCRIPTION
from keyboards import get_back_to_courses_keyboard, get_tariffs_keyboard
from utils.data_loader import get_direction_by_id, load_directions
from utils.image_handler import get_courses_overview_image, get_tariffs_image

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
        text += f"💰 <b>Доход:</b> {course['income']}\n"
        text += f"💳 <b>Цена:</b> {course['price_basic']} / {course['price_with_chat']}\n\n"
        text += "---\n\n"

    # Добавляем общую информацию один раз в конец
    text += f"ℹ️ {COURSE_BENEFITS}"

    # Удаляем предыдущее сообщение и отправляем новое с фото
    await callback.message.delete()

    courses_image = get_courses_overview_image()
    if courses_image:
        await callback.message.answer_photo(
            photo=courses_image,
            caption=text,
            reply_markup=get_back_to_courses_keyboard(dir_id)
        )
    else:
        await callback.message.answer(
            text,
            reply_markup=get_back_to_courses_keyboard(dir_id)
        )

    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def show_tariffs(callback: CallbackQuery):
    """Показать тарифы для покупки."""
    text = f"💳 <b>Тарифы обучения</b>\n\n{TARIFFS_DESCRIPTION}"

    # Удаляем предыдущее сообщение и отправляем новое с фото
    await callback.message.delete()

    tariffs_image = get_tariffs_image()
    if tariffs_image:
        await callback.message.answer_photo(
            photo=tariffs_image,
            caption=text,
            reply_markup=get_tariffs_keyboard()
        )
    else:
        await callback.message.answer(
            text,
            reply_markup=get_tariffs_keyboard()
        )

    await callback.answer()
