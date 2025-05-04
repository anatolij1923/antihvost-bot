from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from database.database import Database

router = Router()

# Создаем клавиатуру главного меню
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="📋 Мои задачи", callback_data="my_tasks")
        ],
        [
            InlineKeyboardButton(text="📅 Календарь", callback_data="calendar")
        ],
        [
            InlineKeyboardButton(text="🏆 Рейтинг", callback_data="rating")
        ],
        [
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Создаем клавиатуру подменю "Мои задачи"
def get_tasks_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_task")
        ],
        [
            InlineKeyboardButton(text="📋 Список задач", callback_data="search_tasks")
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Создаем Reply-клавиатуру с кнопкой "Главное меню"
def get_main_menu_reply_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏠 Главное меню")]],
        resize_keyboard=True
    )
    return keyboard

# Создаем клавиатуру для компактного вида задач
def get_compact_tasks_keyboard(tasks: list) -> InlineKeyboardMarkup:
    keyboard = []
    for task in tasks:
        task_id, title, task_type, subject, deadline, description, priority, status = task
        keyboard.append([
            InlineKeyboardButton(
                text=f"{task_type} {title}",
                callback_data=f"task_detail:{task_id}"
            )
        ])
    
    # Добавляем кнопку для переключения в подробный вид
    keyboard.append([
        InlineKeyboardButton(
            text="📋 Подробный вид",
            callback_data="view_mode:detailed"
        )
    ])
    
    # Добавляем кнопку возврата в меню
    keyboard.append([
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Создаем клавиатуру для подробного вида задач
def get_detailed_tasks_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="📱 Компактный вид",
                callback_data="view_mode:compact"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Назад",
                callback_data="back_to_main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Хендлер для команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
    await message.answer(
        "Вы всегда можете вернуться в главное меню, нажав на кнопку ниже:",
        reply_markup=get_main_menu_reply_keyboard()
    )

# Хендлер для команды /menu
@router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard()
    )
    await message.answer(
        "Вы всегда можете вернуться в главное меню, нажав на кнопку ниже:",
        reply_markup=get_main_menu_reply_keyboard()
    )

# Хендлеры для кнопок меню
@router.callback_query(lambda c: c.data == "my_tasks")
async def process_my_tasks(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Мои задачи:",
        reply_markup=get_tasks_menu_keyboard()
    )

@router.callback_query(lambda c: c.data == "back_to_main")
async def process_back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard()
    )

@router.callback_query(lambda c: c.data == "calendar")
async def process_calendar(callback: types.CallbackQuery):
    await callback.answer("Раздел 'Календарь' в разработке")

@router.callback_query(lambda c: c.data == "rating")
async def process_rating(callback: types.CallbackQuery):
    await callback.answer("Раздел 'Рейтинг' в разработке")

@router.callback_query(lambda c: c.data == "settings")
async def process_settings(callback: types.CallbackQuery):
    await callback.answer("Раздел 'Настройки' в разработке")

@router.callback_query(lambda c: c.data == "search_tasks")
async def process_search_tasks(callback: types.CallbackQuery):
    db = Database()
    tasks = await db.get_user_tasks(callback.from_user.id)
    
    if not tasks:
        await callback.message.edit_text(
            "📋 У вас пока нет активных задач.\n\n"
            "Вы можете добавить новую задачу, нажав на кнопку ниже:",
            reply_markup=get_tasks_menu_keyboard()
        )
        return
    
    # Показываем компактный вид по умолчанию
    message_text = "📋 Ваши активные задачи:\n\n"
    message_text += "Нажмите на задачу, чтобы увидеть подробности."
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_compact_tasks_keyboard(tasks)
    )

@router.callback_query(lambda c: c.data.startswith("view_mode:"))
async def process_view_mode(callback: types.CallbackQuery):
    db = Database()
    tasks = await db.get_user_tasks(callback.from_user.id)
    
    if not tasks:
        await callback.message.edit_text(
            "📋 У вас пока нет активных задач.\n\n"
            "Вы можете добавить новую задачу, нажав на кнопку ниже:",
            reply_markup=get_tasks_menu_keyboard()
        )
        return
    
    view_mode = callback.data.split(":")[1]
    
    if view_mode == "detailed":
        message_text = "📋 Ваши активные задачи:\n\n"
        
        for task in tasks:
            task_id, title, task_type, subject, deadline, description, priority, status = task
            message_text += (
                f"📌 {title}\n"
                f"📋 Тип: {task_type}\n"
            )
            
            if task_type in ["🔬 Лабораторная", "🏠 Домашка"]:
                message_text += f"📚 Дисциплина: {subject}\n"
                
            message_text += (
                f"⏰ Дедлайн: {deadline}\n"
                f"📝 Описание: {description or 'Нет описания'}\n"
                f"⚠️ Приоритет: {priority}\n"
                f"────────────────────\n"
            )
        
        await callback.message.edit_text(
            message_text,
            reply_markup=get_detailed_tasks_keyboard()
        )
    else:  # compact view
        message_text = "📋 Ваши активные задачи:\n\n"
        message_text += "Нажмите на задачу, чтобы увидеть подробности."
        
        await callback.message.edit_text(
            message_text,
            reply_markup=get_compact_tasks_keyboard(tasks)
        )

@router.callback_query(lambda c: c.data.startswith("task_detail:"))
async def process_task_detail(callback: types.CallbackQuery):
    db = Database()
    task_id = int(callback.data.split(":")[1])
    
    # Получаем информацию о конкретной задаче
    try:
        db.cursor.execute('''
            SELECT id, title, task_type, subject, 
                   strftime('%d.%m.%Y %H:%M', deadline) as deadline,
                   description, priority, status
            FROM tasks
            WHERE id = ?
        ''', (task_id,))
        task = db.cursor.fetchone()
        
        if task:
            task_id, title, task_type, subject, deadline, description, priority, status = task
            message_text = (
                f"📌 {title}\n"
                f"📋 Тип: {task_type}\n"
            )
            
            if task_type in ["🔬 Лабораторная", "🏠 Домашка"]:
                message_text += f"📚 Дисциплина: {subject}\n"
                
            message_text += (
                f"⏰ Дедлайн: {deadline}\n"
                f"📝 Описание: {description or 'Нет описания'}\n"
                f"⚠️ Приоритет: {priority}\n"
            )
            
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="◀️ Назад к списку",
                        callback_data="view_mode:compact"
                    )
                ]
            ]
            
            await callback.message.edit_text(
                message_text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        else:
            await callback.answer("Задача не найдена")
    except Exception as e:
        print(f"Error getting task details: {e}")
        await callback.answer("Произошла ошибка при получении информации о задаче")

# Хендлер для кнопки "Главное меню"
@router.message(F.text == "🏠 Главное меню")
async def process_main_menu_button(message: types.Message):
    await message.answer(
        "Главное меню:",
        reply_markup=get_main_menu_keyboard()
    ) 