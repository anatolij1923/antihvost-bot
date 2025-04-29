from aiogram.fsm.state import StatesGroup, State

class AuthStates(StatesGroup):
    waiting_for_fullname = State()
    waiting_for_group = State()
