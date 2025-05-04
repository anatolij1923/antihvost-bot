from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from states.task_states import TaskCreation
from database.database import Database

router = Router()
db = Database()

# Клавиатура для выбора типа задачи
def get_task_type_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="🔬 Лабораторная", callback_data="task_type:lab"),
            InlineKeyboardButton(text="🏠 Домашка", callback_data="task_type:homework")
        ],
        [
            InlineKeyboardButton(text="📅 Мероприятие", callback_data="task_type:event")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатура для выбора дисциплины
def get_subject_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Программирование", callback_data="subject:programming"),
            InlineKeyboardButton(text="Информатика", callback_data="subject:informatics")
        ],
        [
            InlineKeyboardButton(text="Дискретная математика", callback_data="subject:discrete_math")
        ],
        [
            InlineKeyboardButton(text="Ввести вручную", callback_data="subject:manual")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатура для выбора приоритета
def get_priority_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="⚠️ Низкий", callback_data="priority:low"),
            InlineKeyboardButton(text="🟡 Средний", callback_data="priority:medium")
        ],
        [
            InlineKeyboardButton(text="🔴 Высокий", callback_data="priority:high")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатура для подтверждения
def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_task"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_task")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Начало создания задачи
@router.callback_query(lambda c: c.data == "add_task")
async def start_task_creation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Выберите тип задачи:",
        reply_markup=get_task_type_keyboard()
    )
    await state.set_state(TaskCreation.waiting_for_type)

# Обработка типа задачи
@router.callback_query(TaskCreation.waiting_for_type, F.data.startswith("task_type:"))
async def process_type(callback: types.CallbackQuery, state: FSMContext):
    task_type = callback.data.split(":")[1]
    type_names = {
        "lab": "🔬 Лабораторная",
        "homework": "🏠 Домашка",
        "event": "📅 Мероприятие"
    }
    await state.update_data(task_type=type_names[task_type])
    
    if task_type in ["lab", "homework"]:
        await callback.message.edit_text(
            "Выберите дисциплину:",
            reply_markup=get_subject_keyboard()
        )
        await state.set_state(TaskCreation.waiting_for_subject)
    else:  # Для мероприятий
        await state.update_data(subject="Мероприятие")
        await callback.message.edit_text(
            "Введите название мероприятия:"
        )
        await state.set_state(TaskCreation.waiting_for_title)

# Обработка выбора дисциплины
@router.callback_query(TaskCreation.waiting_for_subject, F.data.startswith("subject:"))
async def process_subject(callback: types.CallbackQuery, state: FSMContext):
    subject = callback.data.split(":")[1]
    if subject == "manual":
        await callback.message.edit_text(
            "Введите название дисциплины:"
        )
        await state.set_state(TaskCreation.waiting_for_subject)
    else:
        subject_names = {
            "programming": "Программирование",
            "informatics": "Информатика",
            "discrete_math": "Дискретная математика"
        }
        await state.update_data(subject=subject_names[subject])
        await callback.message.edit_text(
            "Введите название задачи:"
        )
        await state.set_state(TaskCreation.waiting_for_title)

# Обработка ручного ввода дисциплины
@router.message(TaskCreation.waiting_for_subject)
async def process_manual_subject(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer(
        "Введите название задачи:"
    )
    await state.set_state(TaskCreation.waiting_for_title)

# Обработка названия задачи
@router.message(TaskCreation.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        "Введите описание задачи (или отправьте '-' если описание не требуется):"
    )
    await state.set_state(TaskCreation.waiting_for_description)

# Обработка описания
@router.message(TaskCreation.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    description = message.text if message.text != "-" else None
    await state.update_data(description=description)
    await message.answer(
        "Введите дедлайн в формате ДД.ММ.ГГГГ ЧЧ:ММ:"
    )
    await state.set_state(TaskCreation.waiting_for_deadline)

# Обработка дедлайна
@router.message(TaskCreation.waiting_for_deadline)
async def process_deadline(message: types.Message, state: FSMContext):
    try:
        deadline = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        await state.update_data(deadline=deadline)
        await message.answer(
            "Выберите приоритет задачи:",
            reply_markup=get_priority_keyboard()
        )
        await state.set_state(TaskCreation.waiting_for_priority)
    except ValueError:
        await message.answer(
            "Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ ЧЧ:ММ:"
        )

# Обработка приоритета
@router.callback_query(TaskCreation.waiting_for_priority, F.data.startswith("priority:"))
async def process_priority(callback: types.CallbackQuery, state: FSMContext):
    priority = callback.data.split(":")[1]
    priority_names = {
        "low": "⚠️ Низкий",
        "medium": "🟡 Средний",
        "high": "🔴 Высокий"
    }
    await state.update_data(priority=priority_names[priority])
    
    # Получаем все данные
    data = await state.get_data()
    
    # Формируем сообщение с подтверждением
    confirmation_text = (
        f"Проверьте данные задачи:\n\n"
        f"📌 Название: {data['title']}\n"
        f"📋 Тип: {data['task_type']}\n"
    )
    
    if data['task_type'] in ["🔬 Лабораторная", "🏠 Домашка"]:
        confirmation_text += f"📚 Дисциплина: {data['subject']}\n"
    
    confirmation_text += (
        f"⏰ Дедлайн: {data['deadline'].strftime('%d.%m.%Y %H:%M')}\n"
        f"📝 Описание: {data['description'] or 'Нет описания'}\n"
        f"⚠️ Приоритет: {data['priority']}\n\n"
        f"Подтвердите создание задачи:"
    )
    
    await callback.message.edit_text(
        confirmation_text,
        reply_markup=get_confirmation_keyboard()
    )
    await state.set_state(TaskCreation.confirmation)

# Обработка подтверждения
@router.callback_query(TaskCreation.confirmation, F.data == "confirm_task")
async def process_confirmation(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    # Сохраняем задачу в базу данных
    success = await db.add_task(
        user_id=callback.from_user.id,
        title=data['title'],
        task_type=data['task_type'],
        subject=data['subject'],
        deadline=data['deadline'],
        description=data['description'],
        priority=data['priority']
    )
    
    if success:
        await callback.message.edit_text(
            "✅ Задача успешно создана!"
        )
    else:
        await callback.message.edit_text(
            "❌ Произошла ошибка при создании задачи. Пожалуйста, попробуйте позже."
        )
    
    await state.clear()

# Обработка отмены
@router.callback_query(TaskCreation.confirmation, F.data == "cancel_task")
async def process_cancellation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "❌ Создание задачи отменено."
    )
    await state.clear() 