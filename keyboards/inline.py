from typing import List, Dict, Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from constants import (
    BUTTON_BUY_COURSE,
    BUTTON_BUY_INSTALLMENT,
    BUTTON_GET_DETAILS,
    CONSULTATION_URL,
    TARIFFS,
)


def get_directions_keyboard(directions: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Клавиатура с направлениями для заработка."""
    buttons = []
    for direction in directions:
        buttons.append([InlineKeyboardButton(
            text=f"{direction['emoji']} {direction['title']}",
            callback_data=f"dir_{direction['id']}"
        )])
    buttons.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_direction_detail_keyboard(dir_id: str) -> InlineKeyboardMarkup:
    """Детальная клавиатура для направления."""
    buttons = []

    # Специальные кнопки для разных направлений
    if dir_id == "online_specialist":
        buttons.append([InlineKeyboardButton(text="📚 Посмотреть курсы", callback_data=f"courses_{dir_id}")])
    elif dir_id == "marketplace_work":
        buttons.append([InlineKeyboardButton(text="🎨 Дизайнер инфографики", callback_data=f"designer_{dir_id}")])
        buttons.append([InlineKeyboardButton(text="👨‍💼 Менеджер маркетплейсов", callback_data=f"manager_{dir_id}")])
    elif dir_id == "curator_online_school":
        buttons.append([InlineKeyboardButton(text="📚 Подробнее о работе", callback_data=f"curator_details_{dir_id}")])
    elif dir_id == "task_execution":
        buttons.append([InlineKeyboardButton(text="📋 Виды заданий", callback_data=f"tasks_details_{dir_id}")])

    # Общие кнопки для всех направлений - ВАЖНО: добавляем ссылку на консультацию!
    buttons.append([InlineKeyboardButton(text=BUTTON_BUY_COURSE, callback_data=f"buy_{dir_id}")])
    buttons.append([InlineKeyboardButton(text=BUTTON_GET_DETAILS, url=CONSULTATION_URL)])
    buttons.append([InlineKeyboardButton(text="↩️ Назад к направлениям", callback_data="directions")])
    buttons.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_earning_ways_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура способов заработка."""
    buttons = [
        [InlineKeyboardButton(text="📚 Обучение новой онлайн профессии", callback_data="earning_training")],
        [InlineKeyboardButton(text="💼 Направления для заработка", callback_data="directions")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_tariffs_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с тарифами."""
    buttons = []
    for tariff_data in TARIFFS.values():
        buttons.append([InlineKeyboardButton(
            text=f"{tariff_data['name']} {tariff_data['price']}",
            url=tariff_data['url']
        )])

    # ВАЖНО: Добавляем кнопки рассрочки и консультации
    buttons.append([InlineKeyboardButton(text=BUTTON_BUY_INSTALLMENT, url=CONSULTATION_URL)])
    buttons.append([InlineKeyboardButton(text=BUTTON_GET_DETAILS, url=CONSULTATION_URL)])
    buttons.append([InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_to_direction_keyboard(dir_id: str) -> InlineKeyboardMarkup:
    """Клавиатура возврата к направлению."""
    buttons = [
        [InlineKeyboardButton(text=BUTTON_BUY_COURSE, callback_data=f"buy_{dir_id}")],
        [InlineKeyboardButton(text=BUTTON_GET_DETAILS, url=CONSULTATION_URL)],
        [InlineKeyboardButton(text="↩️ Назад", callback_data=f"dir_{dir_id}")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_to_courses_keyboard(dir_id: str) -> InlineKeyboardMarkup:
    """Клавиатура возврата к курсам."""
    buttons = [
        [InlineKeyboardButton(text=BUTTON_BUY_COURSE, callback_data=f"buy_{dir_id}")],
        [InlineKeyboardButton(text=BUTTON_GET_DETAILS, url=CONSULTATION_URL)],
        [InlineKeyboardButton(text="↩️ Назад к направлению", callback_data=f"dir_{dir_id}")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
