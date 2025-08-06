from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from constants import BUTTON_BUY_COURSE, BUTTON_GET_DETAILS, CONSULTATION_URL
from keyboards import get_direction_detail_keyboard, get_directions_keyboard, get_back_to_direction_keyboard
from states import UserStates
from utils.data_loader import get_direction_by_id, load_directions

router = Router()
DIRECTIONS = load_directions()


@router.message(F.text == "💼 Направления для заработка")
async def show_directions(message: Message, state: FSMContext):
    """Показать список направлений для заработка."""
    await state.set_state(UserStates.choosing_direction)
    await message.answer(
        "💼 <b>Направления для заработка</b>\n\n"
        "Выбери интересующее направление, чтобы узнать подробности:",
        reply_markup=get_directions_keyboard(DIRECTIONS)
    )


@router.callback_query(F.data.startswith("dir_"))
async def show_direction_detail(callback: CallbackQuery, state: FSMContext):
    """Показать детали направления."""
    dir_id = callback.data.split("_", 1)[1]
    direction = get_direction_by_id(DIRECTIONS, dir_id)

    if not direction:
        await callback.answer("Направление не найдено")
        return

    await state.set_state(UserStates.viewing_direction)
    await state.update_data(current_direction=dir_id)

    text = f"{direction['emoji']} <b>{direction['title']}</b>\n\n"
    text += direction['description']

    # Добавляем специализации если есть
    if 'specializations' in direction:
        text += "\n\n<b>Специализации:</b>\n"
        for spec in direction['specializations']:
            text += f"• {spec}\n"

    # Добавляем дополнительную информацию в зависимости от направления
    if dir_id == "task_execution":
        text += f"\n\n<b>💰 Доходы:</b>\n"
        text += f"• Одно задание: {direction['income_per_task']}\n"
        text += f"• В день: {direction['daily_tasks']}\n"
        text += f"• В месяц: {direction['monthly_income']}"
    elif dir_id == "curator_online_school":
        text += f"\n\n<b>💰 Доход:</b> {direction['income']}\n"
        text += f"<b>💸 Комиссия:</b> {direction['commission']}"

    await callback.message.edit_text(
        text,
        reply_markup=get_direction_detail_keyboard(dir_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("designer_"))
async def show_designer_info(callback: CallbackQuery):
    """Показать информацию о дизайнере инфографики."""
    text = "🎨 <b>Дизайнер инфографики</b>\n\n"
    text += "Это человек, который оформляет карточки товаров для маркетплейсов — Wildberries, Ozon и др.\n\n"
    text += "Ты делаешь слайды: фото + короткие описания и преимущества — именно то, что видит покупатель, когда выбирает товар.\n\n"
    text += "Работать можно даже с телефона, уделяя в день от 2 часов.\n"
    text += "Компьютер не обязателен, опыт не нужен — всему научишься с нуля благодаря курсам!\n\n"
    text += "💰 <b>Доходы:</b>\n"
    text += "👉🏼 Новички берут от 300–500 ₽ за 1 слайд\n"
    text += "👉🏼 На один товар обычно заказывают 5–10 слайдов\n"
    text += "👉🏼 То есть с одного клиента выходит от 2 000 ₽ и выше\n"
    text += "👉🏼 Уже с 1–2 заказов в неделю можно выйти на доход 30 000 ₽ в месяц"

    await callback.message.edit_text(text, reply_markup=get_back_to_direction_keyboard("marketplace_work"))
    await callback.answer()


@router.callback_query(F.data.startswith("manager_"))
async def show_manager_info(callback: CallbackQuery):
    """Показать информацию о менеджере маркетплейсов."""
    text = "👨‍💼 <b>Менеджер маркетплейсов</b>\n\n"
    text += "— работа в личном кабинете продавца\n"
    text += "— создание карточек, создание описания товаров\n"
    text += "— ответы на отзывы, управление ценами, запуск рекламы\n\n"
    text += "Здесь нужен компьютер — с телефона не получится\n\n"
    text += "💰 <b>Доходы:</b>\n"
    text += "👉🏼 Новички берут от 10 000 до 20 000 ₽ за одного клиента в месяц\n"
    text += "👉🏼 Обычно менеджер ведёт 2–4 магазина одновременно\n"
    text += "👉🏼 То есть на практике доход выходит от 40 000 до 80 000 ₽ в месяц и выше\n"
    text += "(в зависимости от количества клиентов и формата работы)"

    await callback.message.edit_text(text, reply_markup=get_back_to_direction_keyboard("marketplace_work"))
    await callback.answer()


@router.callback_query(F.data.startswith("curator_details_"))
async def show_curator_details(callback: CallbackQuery):
    """Показать детали работы куратора."""
    text = "🎓 <b>Работа куратора онлайн школы</b>\n\n"
    text += "Работа куратора — это:\n"
    text += "— вести соцсети (Instagram, VK, Telegram, Pinterest, Treads)\n"
    text += "— рассказывать в своих соц.сетях о школе и вариантах заработка\n"
    text += "— выстраивать входящий поток — чтобы тебе писали сами, с помощью чат ботов и обратной связи\n"
    text += "— консультировать тех, кому интересно, и подключать к обучению\n\n"
    text += "Можно отвечать вручную, а можно — как я — подключить чат-бота, чтобы часть работы шла автоматически.\n\n"
    text += "Главное — готовность разбираться, не ждать волшебства и реально делать шаги."

    await callback.message.edit_text(text, reply_markup=get_back_to_direction_keyboard("curator_online_school"))
    await callback.answer()


@router.callback_query(F.data.startswith("tasks_details_"))
async def show_tasks_details(callback: CallbackQuery):
    """Показать детали выполнения заданий."""
    direction = get_direction_by_id(DIRECTIONS, 'task_execution')

    text = "✅ <b>Что нужно делать</b>\n\n"
    for task in direction['tasks']:
        text += f"— {task}\n"

    text += "\n<b>Кто вам платит за это?</b>\n\n"
    for payer in direction['who_pays']:
        text += f"— {payer}\n"

    text += f"\n{direction['advantages']}"

    await callback.message.edit_text(text, reply_markup=get_back_to_direction_keyboard("task_execution"))
    await callback.answer()


@router.callback_query(F.data == "directions")
async def back_to_directions(callback: CallbackQuery, state: FSMContext):
    """Вернуться к списку направлений."""
    await state.set_state(UserStates.choosing_direction)
    await callback.message.edit_text(
        "💼 <b>Направления для заработка</b>\n\n"
        "Выбери интересующее направление, чтобы узнать подробности:",
        reply_markup=get_directions_keyboard(DIRECTIONS)
    )
    await callback.answer()
