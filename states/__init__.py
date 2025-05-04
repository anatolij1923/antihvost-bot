from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    main_menu = State()
    assignments = State()
    events = State()
    profile = State()

__all__ = ['UserStates'] 