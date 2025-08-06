from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import get_main_menu

router = Router()


@router.message(F.text == "⚙️ Настройки")
async def show_settings(message: Message):
    """Показать настройки бота."""
    await message.answer(
        "⚙️ <b>Настройки</b>\n\n"
        "🎯 Выбор интересующих направлений\n"
        "📊 Уровень опыта\n"
        "🔔 Уведомления\n"
        "👤 Профиль\n\n"
        "⚠️ <i>Функционал настроек будет добавлен в следующих версиях</i>"
    )


@router.message(F.text == "ℹ️ О боте")
async def show_about(message: Message):
    """Показать информацию о боте."""
    text = "ℹ️ <b>О боте</b>\n\n"
    text += "🎯 Этот бот поможет тебе найти свой путь в мире фриланса и удаленной работы.\n\n"
    text += "<b>Что умеет бот:</b>\n"
    text += "• Показывает 4 основных направления для заработка\n"
    text += "• Предоставляет информацию о курсах и обучении\n"
    text += "• Помогает выбрать подходящий тариф\n"
    text += "• Подключает к консультациям с экспертом\n"
    text += "• Дает практические советы для старта\n\n"
    text += "💬 <b>Поддержка:</b> @Anfikus\n"
    text += "📈 <b>Версия:</b> 2.0"

    await message.answer(text)


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """Вернуться в главное меню."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "🏠 <b>Главное меню</b>\n\n"
        "Выбери интересующий раздел:",
        reply_markup=get_main_menu()
    )
    await callback.answer()
