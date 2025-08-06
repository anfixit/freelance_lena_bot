from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    choosing_direction = State()
    viewing_direction = State()
    viewing_courses = State()
    viewing_earning_ways = State()
    settings = State()
