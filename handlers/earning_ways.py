from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import get_earning_ways_keyboard
from states import UserStates

router = Router()


@router.message(F.text == "💰 Способы заработка")
async def show_earning_ways(message: Message, state: FSMContext):
    """Показать способы заработка."""
    await state.set_state(UserStates.viewing_earning_ways)
    text = "💰 <b>Способы заработка</b>\n\n"
    text += "Выбери, что тебя интересует:"

    await message.answer(text, reply_markup=get_earning_ways_keyboard())


@router.callback_query(F.data == "earning_training")
async def show_earning_training(callback: CallbackQuery):
    """Показать обучение как способ заработка."""
    # Импортируем функцию из courses.py
    from .courses import show_tariffs
    await show_tariffs(callback)
