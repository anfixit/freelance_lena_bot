from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from constants import TARIFFS_DESCRIPTION
from keyboards import get_back_to_courses_keyboard, get_tariffs_keyboard
from utils.data_loader import get_direction_by_id, load_directions
from utils.image_handler import get_tariffs_image

router = Router()
DIRECTIONS = load_directions()


def truncate_text(text: str, max_length: int = 900) -> str:
    """Обрезает текст до максимальной длины."""
    if len(text) <= max_length:
        return text

    # Находим последнее место для обрезки (по точке или переносу строки)
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    last_newline = truncated.rfind('\n')

    cut_point = max(last_period, last_newline)
    if cut_point > max_length - 200:  # Если точка/перенос не слишком далеко
        return text[:cut_point + 1] + "\n\n... (продолжение в консультации)"
    else:
        return text[:max_length] + "..."


@router.callback_query(F.data.startswith("courses_"))
async def show_courses(callback: CallbackQuery):
    """Показать курсы для направления."""
    dir_id = callback.data.split("_", 1)[1]
    direction = get_direction_by_id(DIRECTIONS, dir_id)

    if not direction or 'courses' not in direction:
        await callback.answer("Курсы не найдены")
        return

    text = f"📚 <b>Курсы: {direction['title']}</b>\n\n"

    for i, course in enumerate(direction['courses']):
        text += f"🎓 <b>{course['name']}</b>\n"

        # Сокращаем описание курса
        short_description = truncate_text(course['description'], 300)
        text += f"{short_description}\n\n"

        text += f"💰 <b>Доход:</b> {course['income']}\n"
        text += f"💳 <b>Цена:</b> {course['price_basic']} / {course['price_with_chat']}\n\n"

        if i < len(direction['courses']) - 1:  # Не добавляем разделитель после последнего курса
            text += "---\n\n"

    # Проверяем общую длину
    if len(text) > 900:
        text = truncate_text(text, 900)

    await callback.message.edit_text(text, reply_markup=get_back_to_courses_keyboard(dir_id))
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def show_tariffs(callback: CallbackQuery):
    """Показать тарифы для покупки с картинкой."""
    try:
        # Пытаемся получить картинку тарифов
        photo = get_tariffs_image()

        # Сокращаем текст описания тарифов
        short_description = truncate_text(TARIFFS_DESCRIPTION, 800)

        text = f"💳 <b>Тарифы обучения</b>\n\n{short_description}"

        if photo:
            await callback.message.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=get_tariffs_keyboard()
            )
            # Удаляем предыдущее сообщение
            try:
                await callback.message.delete()
            except:
                pass
        else:
            # Если картинки нет - отправляем обычным текстом
            await callback.message.edit_text(text, reply_markup=get_tariffs_keyboard())

    except Exception as e:
        # Если ошибка с картинкой - отправляем просто текст
        text = f"💳 <b>Тарифы обучения</b>\n\n{truncate_text(TARIFFS_DESCRIPTION, 900)}"
        await callback.message.edit_text(text, reply_markup=get_tariffs_keyboard())

    await callback.answer()


# Добавляем новый хэндлер для показа тарифов из earning_ways
@router.callback_query(F.data == "earning_training")
async def show_tariffs_from_earning(callback: CallbackQuery):
    """Показать тарифы при выборе 'Обучение новой профессии'."""
    await show_tariffs(callback)
