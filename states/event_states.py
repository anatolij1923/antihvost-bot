from aiogram.fsm.state import StatesGroup, State

class EventStates(StatesGroup):
    entering_name = State()
    entering_description = State()
    entering_date = State() 