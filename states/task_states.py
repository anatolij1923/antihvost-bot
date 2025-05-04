from aiogram.fsm.state import State, StatesGroup

class TaskCreation(StatesGroup):
    waiting_for_title = State()
    waiting_for_type = State()
    waiting_for_subject = State()
    waiting_for_deadline = State()
    waiting_for_description = State()
    waiting_for_priority = State()
    confirmation = State() 