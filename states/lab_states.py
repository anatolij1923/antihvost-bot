from aiogram.fsm.state import State, StatesGroup

class AssignmentStates(StatesGroup):
    choosing_type = State()        # Выбор типа задания (лаба/домашка)
    entering_name = State()        # Ввод названия задания
    entering_description = State() # Ввод описания
    entering_deadline = State()    # Установка дедлайна
    choosing_status = State()  # Новое состояние для выбора статуса
