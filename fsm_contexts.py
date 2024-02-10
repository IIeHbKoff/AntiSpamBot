from aiogram.fsm.state import StatesGroup, State


class CapchaState(StatesGroup):
    on_verification = State()

